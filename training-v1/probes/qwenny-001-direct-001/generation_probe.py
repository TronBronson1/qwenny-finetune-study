"""Secondary direct-answer pilot and fresh adapter import checks; not formal held-out evaluation."""
import argparse, contextlib, json, pathlib, re, shutil, time, traceback
import torch
from peft import PeftModel
from transformers import LogitsProcessor,LogitsProcessorList
from runtime import ROOT,EXP,load_base,tokenizer,Monitor,memory

class OutputPresencePenalty(LogitsProcessor):
    def __init__(self,prompt_length,penalty,progress_path=None): self.prompt_length=prompt_length; self.penalty=penalty; self.progress_path=progress_path
    def __call__(self,input_ids,scores):
        count=input_ids.shape[1]-self.prompt_length
        if self.progress_path and count%128==0:
            self.progress_path.write_text(json.dumps({'generated_tokens':count,'unix_time':time.time()}),encoding='utf-8')
        for index in range(input_ids.shape[0]):
            seen=input_ids[index,self.prompt_length:].unique()
            scores[index,seen]-=self.penalty
        return scores

def write(path,value): path.write_text(json.dumps(value,indent=2),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--training-run",required=True); p.add_argument("--out",required=True)
    p.add_argument("--tasks",nargs="+",default=["DV001","DV002"]); p.add_argument("--thinking",action="store_true")
    p.add_argument("--max-new-tokens",type=int,default=2048)
    a=p.parse_args(); out=(ROOT/a.out).resolve(); assert ROOT in out.parents and not out.exists()
    run=ROOT/a.training_run; trained=json.loads((run/"report.json").read_text()); assert trained["status"]=="trained"
    out.mkdir(parents=True)
    report={"status":"loading","scope":"Secondary generation/import pilot only; direct-answer default is separate from the historical thinking-on uncapped LM Studio comparison. Final-test and regression tasks are not scored.","thinking":a.thinking,"seed":42,"temperature":1.0,"top_k":20,"top_p":.95,"presence_penalty":1.5,"presence_definition":"Subtract 1.5 from tokens appearing anywhere in generated output only; not a claim of identical LM Studio penalty implementation.","max_new_tokens":a.max_new_tokens,"context_limit":16134,"completed":[]}
    write(out/"report.json",report); monitor=Monitor(out)
    try:
        shutil.copyfile(ROOT/"generation_probe.py",out/"generation_probe.py")
        shutil.copyfile(ROOT/"runtime.py",out/"runtime.py")
        tok=tokenizer(); base=load_base(training=False)
        model=PeftModel.from_pretrained(base,run/"checkpoints"/"epoch-1",adapter_name="epoch-1",is_trainable=False)
        for epoch in (3,5): model.load_adapter(run/"checkpoints"/f"epoch-{epoch}",adapter_name=f"epoch-{epoch}",is_trainable=False)
        reload_checks=[]
        for epoch in (1,3,5):
            model.set_adapter(f"epoch-{epoch}"); model.eval(); model.requires_grad_(False)
            probe=torch.load(run/"checkpoints"/f"epoch-{epoch}"/"reload-probe.pt",map_location="cpu",weights_only=True)
            with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                logits=model(input_ids=probe["input_ids"].to("cuda"),use_cache=False,logits_to_keep=1).logits.float().cpu()
            delta=(logits-probe["logits"]).abs().max().item()
            assert torch.allclose(logits,probe["logits"],atol=.02,rtol=.01),f"Reload failed epoch {epoch}"
            reload_checks.append({"epoch":epoch,"max_abs_logit_difference":delta,"passed":True})
        write(out/"reload_checks.json",reload_checks)
        report["reload_checks"]=reload_checks; report["status"]="generating"; write(out/"report.json",report)
        corpus=EXP/"dataset-v1"/"candidate-006"
        requests=[json.loads(line) for line in (corpus/"model-packets"/"development-requests.jsonl").read_text(encoding="utf-8").splitlines()]
        requests={r["id"]:r for r in requests}
        assert all(t in requests for t in a.tasks)
        demonstrations=[]
        for ident in ("D01","D02"):
            folder=EXP/"prompt-comparison"/"demonstrations"/ident
            demonstrations += [{"role":"user","content":(folder/"SPEC.md").read_text(encoding="utf-8").strip()},{"role":"assistant","content":(folder/"ANSWER.md").read_text(encoding="utf-8").strip()}]
        variants=[("base-A",None,False),("base-B",None,True),("epoch-1-C","epoch-1",False),("epoch-3-C","epoch-3",False),("epoch-5-C","epoch-5",False)]
        stops=[tok.convert_tokens_to_ids("<|im_end|>"),tok.convert_tokens_to_ids("<|endoftext|>")]
        for task_index,task in enumerate(a.tasks):
            ordered=variants[task_index%len(variants):]+variants[:task_index%len(variants)]
            for label,adapter,with_demos in ordered:
                folder=out/task/label; folder.mkdir(parents=True)
                messages=requests[task]["messages"]
                if with_demos: messages=[messages[0]]+demonstrations+messages[1:]
                write(folder/"messages.json",messages)
                prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=a.thinking)
                inputs=tok(prompt,return_tensors="pt",add_special_tokens=False).to("cuda")
                length=inputs["input_ids"].shape[1]
                assert length<16134
                limit=min(a.max_new_tokens,16134-length)
                if adapter: model.set_adapter(adapter)
                model.eval(); model.requires_grad_(False)
                torch.manual_seed(42); torch.cuda.manual_seed_all(42)
                report.update(current_task=task,current_variant=label); write(out/"report.json",report)
                context=contextlib.nullcontext() if adapter else model.disable_adapter()
                start=time.monotonic()
                with context,torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                    generated=model.generate(**inputs,do_sample=True,temperature=1.,top_k=20,top_p=.95,max_new_tokens=limit,use_cache=True,eos_token_id=stops,pad_token_id=tok.pad_token_id,logits_processor=LogitsProcessorList([OutputPresencePenalty(length,1.5,folder/'progress.json')]))
                tail=generated[0,length:]; raw=tok.decode(tail,skip_special_tokens=False,clean_up_tokenization_spaces=False)
                terminated=int(tail[-1]) in stops
                (folder/"output.raw.txt").write_text(raw,encoding="utf-8")
                visible=raw.rsplit("</think>",1)[-1]
                for token in ("<|im_end|>","<|endoftext|>"): visible=visible.replace(token,"")
                (folder/"answer.md").write_text(visible,encoding="utf-8")
                fence=chr(96)*3
                blocks=re.findall(fence+r"(?:python|py)?[ \t]*\n(.*?)"+fence,visible,re.S)
                if len(blocks)==1: (folder/"test_candidate.py").write_text(blocks[0],encoding="utf-8")
                item={"task":task,"variant":label,"prompt_tokens":length,"generated_tokens":len(tail),"seconds":time.monotonic()-start,"terminated":terminated,"truncated":not terminated,"python_blocks":len(blocks),"strict_acceptance":"not scored; code and category review required","memory":memory()}
                write(folder/"generation.json",item); report["completed"].append(item); write(out/"report.json",report)
                del inputs,generated,tail
                torch.cuda.empty_cache()
        report["status"]="completed"; write(out/"report.json",report)
    except BaseException as e:
        report.update(status="failed",error=repr(e)); (out/"traceback.txt").write_text(traceback.format_exc(),encoding="utf-8"); write(out/"report.json",report); raise
    finally: monitor.close()

if __name__=="__main__": main()
