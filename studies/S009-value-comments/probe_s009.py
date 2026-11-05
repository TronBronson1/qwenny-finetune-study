"""Frozen S006 local diagnostic. No optimizer updates or final/regression reads."""
import contextlib,hashlib,json,pathlib,re,shutil,time,traceback,sys,platform
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/"training-v1"))
import torch,transformers,peft
from peft import PeftModel
from transformers import LogitsProcessor,LogitsProcessorList,StoppingCriteria,StoppingCriteriaList
from runtime import ROOT,EXP,load_base,tokenizer,verify_checkpoint,Monitor,memory

STUDY=EXP/"studies/S009-value-comments"
OUT=STUDY/"inference-001"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8")
class Progress(LogitsProcessor):
    def __init__(self,length,folder,tok): self.length=length; self.folder=folder; self.tok=tok
    def __call__(self,input_ids,scores):
        n=input_ids.shape[1]-self.length
        if n%128==0:
            write(self.folder/"progress.json",dict(generated_tokens=n,unix_time=time.time()))
            (self.folder/"partial.raw.txt").write_text(self.tok.decode(input_ids[0,self.length:],skip_special_tokens=False,clean_up_tokenization_spaces=False),encoding="utf-8")
        return scores
class Deadline(StoppingCriteria):
    def __init__(self,deadline): self.deadline=deadline
    def __call__(self,input_ids,scores,**kwargs): return time.monotonic()>=self.deadline

def main():
    assert not OUT.exists(),"Never overwrite or resume scored first attempts"
    frozen=json.loads((STUDY/"freeze-manifest.json").read_text(encoding="utf-8"))
    for relative,digest in frozen["files"].items():
        assert sha(EXP/relative)==digest,relative
    selection=json.loads((STUDY/"selection.json").read_text(encoding="utf-8"))["tasks"]
    assert len(selection)==8 and {x["split"] for x in selection}=={"training","development"}
    OUT.mkdir(parents=True)
    report=dict(status="preflight",study="S009",run="inference-001",scope="Exploratory familiar training / development generation diagnostic, not final evaluation.",completed=[],unattempted=[],settings=dict(thinking=False,seed=42,temperature=1.,top_k=20,top_p=.95,presence_penalty=0.,repetition_penalty=1.,max_new_tokens=2048,context_limit=16134,cell_seconds=300,total_seconds=7200),environment=dict(python=sys.version,executable=sys.executable,torch=torch.__version__,transformers=transformers.__version__,peft=peft.__version__,platform=platform.platform()),freeze_manifest_sha256=sha(STUDY/"freeze-manifest.json"))
    write(OUT/"report.json",report)
    monitor=Monitor(OUT); started=time.monotonic(); global_deadline=started+7200
    try:
        shutil.copyfile(pathlib.Path(__file__),OUT/"probe_s009.py")
        shutil.copyfile(ROOT/"runtime.py",OUT/"runtime.py")
        shutil.copyfile(STUDY/"freeze-manifest.json",OUT/"freeze-manifest.json")
        verify_checkpoint()
        from s009_bindings import verify_frozen
        verify_frozen()
        tok=tokenizer(); stops=[tok.convert_tokens_to_ids(t) for t in ("<|im_end|>","<|endoftext|>")]
        assert stops==[248046,248044]
        runs={"baseline":ROOT/"runs/qwenny-003-calibrated-baseline","comments":ROOT/"runs/qwenny-004-value-comments"}
        for run in runs.values(): assert json.loads((run/"report.json").read_text())["status"]=="trained"
        model=None; checks=[]
        for arm,run in runs.items():
            for epoch in (1,3,5):
                name=f"{arm}-e{epoch}"; folder=run/"checkpoints"/f"epoch-{epoch}"
                if model is None: model=PeftModel.from_pretrained(load_base(False),folder,adapter_name=name,is_trainable=False)
                else: model.load_adapter(folder,adapter_name=name,is_trainable=False)
                model.set_adapter(name); model.eval(); model.requires_grad_(False)
                probe=torch.load(folder/"reload-probe.pt",map_location="cpu",weights_only=True)
                with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                    logits=model(input_ids=probe["input_ids"].to("cuda"),use_cache=False,logits_to_keep=1).logits.float().cpu()
                delta=(logits-probe["logits"]).abs().max().item()
                checks.append(dict(arm=arm,epoch=epoch,max_abs_logit_difference=delta,passed=delta==0.))
                write(OUT/"reload_checks.json",checks)
                assert delta==0.,("Exact saved probe mismatch",arm,epoch,delta)
        report["reload_checks"]=checks
        tasks=selection
        variants=[("base",None),("baseline-e5","baseline-e5"),("comments-e5","comments-e5")]
        cells=[]
        for index,row in enumerate(tasks):
            ordered=variants[index%3:]+variants[:index%3]
            cells.extend((row,label,adapter) for label,adapter in ordered)
        for index,(row,label,adapter) in enumerate(cells):
            if time.monotonic()>=global_deadline:
                report["unattempted"]=[dict(task=x["id"],variant=v,reason="study-wall-time-limit") for x,v,_ in cells[index:]]
                report["status"]="stopped-budget"; break
            task=row["id"]; folder=OUT/task/label; folder.mkdir(parents=True)
            source=STUDY/"inputs"/task
            for name in ("messages.json","prompt.txt","prompt-token-ids.json"): shutil.copyfile(source/name,folder/name)
            ids=json.loads((source/"prompt-token-ids.json").read_text(encoding="utf-8"))
            inputs=dict(input_ids=torch.tensor([ids],device="cuda"),attention_mask=torch.ones((1,len(ids)),dtype=torch.long,device="cuda"))
            assert len(ids)+2048<=16134
            if adapter: model.set_adapter(adapter)
            model.eval(); model.requires_grad_(False)
            report.update(status="generating",current_task=task,current_variant=label); write(OUT/"report.json",report)
            torch.manual_seed(42); torch.cuda.manual_seed_all(42)
            begin=time.monotonic(); deadline=min(begin+300,global_deadline)
            context=contextlib.nullcontext() if adapter else model.disable_adapter()
            with context,torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                generated=model.generate(**inputs,do_sample=True,temperature=1.,top_k=20,top_p=.95,repetition_penalty=1.,max_new_tokens=2048,use_cache=True,eos_token_id=stops,pad_token_id=tok.pad_token_id,logits_processor=LogitsProcessorList([Progress(len(ids),folder,tok)]),stopping_criteria=StoppingCriteriaList([Deadline(deadline)]))
            tail=generated[0,len(ids):]; token_ids=tail.tolist()
            raw=tok.decode(tail,skip_special_tokens=False,clean_up_tokenization_spaces=False)
            (folder/"output.raw.txt").write_text(raw,encoding="utf-8"); write(folder/"output-token-ids.json",token_ids)
            terminated=bool(token_ids and token_ids[-1] in stops)
            reasoning_ok="<think>" not in raw or "</think>" in raw
            visible=raw.rsplit("</think>",1)[-1] if reasoning_ok else ""
            for stop in ("<|im_end|>","<|endoftext|>"): visible=visible.replace(stop,"")
            (folder/"answer.md").write_text(visible,encoding="utf-8")
            fence=chr(96)*3
            blocks=re.findall(fence+r"(?:python|py)?[ \t]*\n(.*?)"+fence,visible,re.S)
            if len(blocks)==1: (folder/"test_candidate.py").write_text(blocks[0],encoding="utf-8")
            reason="eos" if terminated else "token-cap" if len(token_ids)>=2048 else "wall-time-limit"
            item=dict(task=task,split=row["split"],family=row["family"],variant=label,prompt_tokens=len(ids),prompt_ids_sha256=sha(folder/"prompt-token-ids.json"),generated_tokens=len(token_ids),seconds=time.monotonic()-begin,terminated=terminated,truncated=not terminated,stop_reason=reason,python_blocks=len(blocks),reasoning_extraction_valid=reasoning_ok,output_sha256=sha(folder/"output.raw.txt"),memory=memory())
            write(folder/"generation.json",item); report["completed"].append(item); write(OUT/"report.json",report)
            print(json.dumps(item),flush=True)
            del inputs,generated,tail; torch.cuda.empty_cache()
        else: report["status"]="completed"
        report["elapsed_seconds"]=time.monotonic()-started; write(OUT/"report.json",report)
    except BaseException as error:
        report.update(status="failed",error=repr(error),elapsed_seconds=time.monotonic()-started)
        (OUT/"traceback.txt").write_text(traceback.format_exc(),encoding="utf-8"); write(OUT/"report.json",report); raise
    finally: monitor.close()
if __name__=="__main__": main()

