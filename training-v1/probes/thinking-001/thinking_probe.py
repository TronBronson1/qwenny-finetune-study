"""Predeclared thinking-enabled development control; preserves every first attempt."""
import contextlib, hashlib, json, re, shutil, time, traceback
import torch
from peft import PeftModel
from transformers import LogitsProcessorList
from runtime import ROOT, load_base, tokenizer, Monitor, memory, verify_checkpoint
from investigate_gap import Progress

def write(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')

def main():
    out=ROOT/'probes/thinking-001'
    assert not out.exists()
    out.mkdir(parents=True)
    report=dict(status='verifying', scope='Two visible development families; bounded local thinking-enabled control, not historical LM Studio replication or final-test evaluation.', thinking=True, seed=42, temperature=1., top_k=20, top_p=.95, presence_penalty=0., repetition_penalty=1., max_new_tokens=8192, context_limit=16134, completed=[])
    write(out/'report.json', report)
    monitor=Monitor(out)
    try:
        for name in ('thinking_probe.py','runtime.py','investigate_gap.py','THINKING_CONTROL_PLAN.md'):
            shutil.copyfile(ROOT/name, out/name)
        verify_checkpoint()
        tok=tokenizer()
        model=PeftModel.from_pretrained(load_base(False), ROOT/'runs/qwenny-001/checkpoints/epoch-5', adapter_name='original-e5', is_trainable=False)
        model.load_adapter(ROOT/'runs/qwenny-002-compact/checkpoints/epoch-5', adapter_name='compact-e5', is_trainable=False)
        checks=[]
        for label, run in [('original-e5','qwenny-001'), ('compact-e5','qwenny-002-compact')]:
            model.set_adapter(label); model.eval(); model.requires_grad_(False)
            probe=torch.load(ROOT/f'runs/{run}/checkpoints/epoch-5/reload-probe.pt', map_location='cpu', weights_only=True)
            with torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
                logits=model(input_ids=probe['input_ids'].to('cuda'), use_cache=False, logits_to_keep=1).logits.float().cpu()
            delta=(logits-probe['logits']).abs().max().item()
            assert torch.allclose(logits, probe['logits'], atol=.02, rtol=.01)
            checks.append(dict(adapter=label, max_abs_logit_difference=delta, passed=True))
        write(out/'reload_checks.json', checks); report['reload_checks']=checks
        stops=[tok.convert_tokens_to_ids(t) for t in ('<|im_end|>','<|endoftext|>')]
        for index, task in enumerate(('DV001','DV002')):
            labels=['base','original-e5','compact-e5']
            labels=labels[index:]+labels[:index]
            messages=json.loads((ROOT/f'investigations/gap-001/{task}/epoch-5-sample-0/messages.json').read_text(encoding='utf-8'))
            prompt=tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
            assert prompt.endswith('<think>\n'), repr(prompt[-100:])
            for label in labels:
                folder=out/task/label; folder.mkdir(parents=True)
                write(folder/'messages.json', messages)
                (folder/'prompt.txt').write_text(prompt, encoding='utf-8')
                inputs=tok(prompt, return_tensors='pt', add_special_tokens=False).to('cuda')
                length=inputs['input_ids'].shape[1]
                assert length+8192<=16134
                if label!='base': model.set_adapter(label)
                model.eval(); model.requires_grad_(False)
                torch.manual_seed(42); torch.cuda.manual_seed_all(42)
                report.update(status='generating', current_task=task, current_variant=label); write(out/'report.json', report)
                start=time.monotonic()
                context=model.disable_adapter() if label=='base' else contextlib.nullcontext()
                with context, torch.no_grad(), torch.autocast('cuda', dtype=torch.bfloat16):
                    generated=model.generate(**inputs, do_sample=True, temperature=1., top_k=20, top_p=.95, max_new_tokens=8192, repetition_penalty=1., use_cache=True, eos_token_id=stops, pad_token_id=tok.pad_token_id, logits_processor=LogitsProcessorList([Progress(length, folder/'progress.json')]))
                ids=generated[0,length:].tolist()
                raw=tok.decode(ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                write(folder/'output_token_ids.json', ids)
                (folder/'output.raw.txt').write_text(raw, encoding='utf-8')
                closed='</think>' in raw
                visible=raw.split('</think>',1)[1] if closed else ''
                for token in ('<|im_end|>','<|endoftext|>'): visible=visible.replace(token,'')
                (folder/'answer.md').write_text(visible, encoding='utf-8')
                fence=chr(96)*3
                blocks=re.findall(fence+r'(?:python|py)?[ \t]*\n(.*?)'+fence, visible, re.S)
                if len(blocks)==1: (folder/'test_candidate.py').write_text(blocks[0], encoding='utf-8')
                close_id=tok.convert_tokens_to_ids('</think>')
                close_at=ids.index(close_id) if close_id in ids else None
                item=dict(task=task, variant=label, prompt_tokens=length, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), generated_tokens=len(ids), reasoning_tokens_before_close=close_at, final_tokens_after_close=len(ids)-close_at-1 if close_at is not None else 0, thinking_closed=closed, seconds=time.monotonic()-start, terminated=ids[-1] in stops, truncated=ids[-1] not in stops, python_blocks=len(blocks), memory=memory())
                write(folder/'generation.json', item); report['completed'].append(item); write(out/'report.json', report)
                del inputs, generated
                torch.cuda.empty_cache()
        report['status']='completed'; write(out/'report.json',report)
    except BaseException as error:
        report.update(status='failed', error=repr(error)); write(out/'report.json',report)
        (out/'traceback.txt').write_text(traceback.format_exc(), encoding='utf-8'); raise
    finally: monitor.close()

if __name__=='__main__': main()
