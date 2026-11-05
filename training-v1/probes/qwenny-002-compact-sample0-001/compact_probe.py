"""Predeclared compact-E5 sample-zero pilot plus fresh import verification."""
import argparse,json,re,shutil,time,traceback
import torch
from peft import PeftModel
from transformers import LogitsProcessorList
from runtime import ROOT,load_base,tokenizer,Monitor,memory
from investigate_gap import Progress

def write(path,data): path.write_text(json.dumps(data,indent=2),encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--run',default='runs/qwenny-002-compact'); parser.add_argument('--out',default='probes/qwenny-002-compact-sample0-001'); a=parser.parse_args()
    run=ROOT/a.run; out=ROOT/a.out; assert not out.exists()
    trained=json.loads((run/'report.json').read_text()); assert trained['status']=='trained'
    out.mkdir(parents=True); monitor=Monitor(out)
    report=dict(status='loading',scope='Predeclared compact-format E5 diagnostic on two visible development tasks; no final evaluation.',training_run=a.run,thinking=False,seed=42,temperature=1.,top_k=20,top_p=.95,presence_penalty=0.,repetition_penalty=1.,max_new_tokens=2048,context_limit=16134,completed=[])
    write(out/'report.json',report)
    try:
        for name in ('compact_probe.py','runtime.py','investigate_gap.py'): shutil.copyfile(ROOT/name,out/name)
        tok=tokenizer(); model=PeftModel.from_pretrained(load_base(False),run/'checkpoints/epoch-1',adapter_name='epoch-1',is_trainable=False)
        for epoch in (3,5): model.load_adapter(run/'checkpoints'/f'epoch-{epoch}',adapter_name=f'epoch-{epoch}',is_trainable=False)
        checks=[]
        for epoch in (1,3,5):
            model.set_adapter(f'epoch-{epoch}'); model.eval(); model.requires_grad_(False)
            probe=torch.load(run/'checkpoints'/f'epoch-{epoch}'/'reload-probe.pt',map_location='cpu',weights_only=True)
            with torch.no_grad(),torch.autocast('cuda',dtype=torch.bfloat16):
                logits=model(input_ids=probe['input_ids'].to('cuda'),use_cache=False,logits_to_keep=1).logits.float().cpu()
            difference=(logits-probe['logits']).abs().max().item()
            assert torch.allclose(logits,probe['logits'],atol=.02,rtol=.01),(epoch,difference)
            checks.append(dict(epoch=epoch,max_abs_logit_difference=difference,passed=True))
        write(out/'reload_checks.json',checks); report['reload_checks']=checks
        model.set_adapter('epoch-5'); model.eval(); model.requires_grad_(False)
        stops=[tok.convert_tokens_to_ids(t) for t in ('<|im_end|>','<|endoftext|>')]
        for task in ('DV001','DV002'):
            label='compact-epoch-5-sample-0'; folder=out/task/label; folder.mkdir(parents=True)
            messages=json.loads((ROOT/'investigations/gap-001'/task/'epoch-5-sample-0/messages.json').read_text(encoding='utf-8')); write(folder/'messages.json',messages)
            prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
            inputs=tok(prompt,return_tensors='pt',add_special_tokens=False).to('cuda'); length=inputs['input_ids'].shape[1]; assert length<16134
            report.update(status='generating',current_task=task,current_variant=label); write(out/'report.json',report)
            torch.manual_seed(42); torch.cuda.manual_seed_all(42); start=time.monotonic()
            with torch.no_grad(),torch.autocast('cuda',dtype=torch.bfloat16):
                generated=model.generate(**inputs,do_sample=True,temperature=1.,top_k=20,top_p=.95,max_new_tokens=min(2048,16134-length),repetition_penalty=1.,use_cache=True,eos_token_id=stops,pad_token_id=tok.pad_token_id,logits_processor=LogitsProcessorList([Progress(length,folder/'progress.json')]))
            tail=generated[0,length:]; raw=tok.decode(tail,skip_special_tokens=False,clean_up_tokenization_spaces=False)
            terminated=int(tail[-1]) in stops; (folder/'output.raw.txt').write_text(raw,encoding='utf-8')
            visible=raw.rsplit('</think>',1)[-1]
            for token in ('<|im_end|>','<|endoftext|>'): visible=visible.replace(token,'')
            (folder/'answer.md').write_text(visible,encoding='utf-8'); fence=chr(96)*3
            blocks=re.findall(fence+r'(?:python|py)?[ \t]*\n(.*?)'+fence,visible,re.S)
            if len(blocks)==1: (folder/'test_candidate.py').write_text(blocks[0],encoding='utf-8')
            item=dict(task=task,variant=label,prompt_tokens=length,generated_tokens=len(tail),seconds=time.monotonic()-start,terminated=terminated,truncated=not terminated,python_blocks=len(blocks),memory=memory())
            write(folder/'generation.json',item); report['completed'].append(item); write(out/'report.json',report)
            del inputs,generated,tail; torch.cuda.empty_cache()
        report['status']='completed'; write(out/'report.json',report)
    except BaseException as error:
        report.update(status='failed',error=repr(error)); (out/'traceback.txt').write_text(traceback.format_exc(),encoding='utf-8'); write(out/'report.json',report); raise
    finally: monitor.close()
if __name__=='__main__': main()
