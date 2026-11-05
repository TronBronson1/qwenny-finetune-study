"""Development-only likelihood/decoding ablation. No optimizer or final-test data."""
import argparse,ast,contextlib,hashlib,json,math,pathlib,re,shutil,time,traceback
import torch
from peft import PeftModel
from transformers import LogitsProcessor,LogitsProcessorList
from transformers.generation.logits_process import TopKLogitsWarper,TopPLogitsWarper
from runtime import ROOT,EXP,load_base,tokenizer,Monitor,memory
from prepare_data import encode_answer

class Progress(LogitsProcessor):
    def __init__(self,length,path): self.length=length; self.path=path
    def __call__(self,ids,scores):
        count=ids.shape[1]-self.length
        if count%128==0: self.path.write_text(json.dumps({"generated_tokens":count,"unix_time":time.time()}))
        return scores

def write(path,value): path.write_text(json.dumps(value,indent=2),encoding="utf-8")

def categories(code,start):
    lines=code.splitlines(keepends=True); offsets=[0]
    for line in lines: offsets.append(offsets[-1]+len(line))
    def point(line,column):
        return offsets[line-1]+len(lines[line-1].encode("utf-8")[:column].decode("utf-8"))
    def span(node):
        return (start+point(node.lineno,node.col_offset),start+point(node.end_lineno,node.end_col_offset))
    regions=[]
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
            if isinstance(node.func.value,ast.Name) and node.func.value.id=="pytest" and node.func.attr=="param":
                if node.args: regions.append(("literal_inputs",*span(node.args[0])))
                if len(node.args)>1: regions.append(("expected_value_literals",*span(node.args[1])))
            if isinstance(node.func.value,ast.Name) and node.func.value.id=="pytest" and node.func.attr=="raises" and node.args:
                regions.append(("expected_exception_class",*span(node.args[0])))
        if isinstance(node,ast.Assert) and "type(" in ast.unparse(node.test):
            regions.append(("exact_type_assertion",*span(node)))
    return regions

def token_groups(full,offsets,code,start):
    regions=categories(code,start)
    priority=["expected_value_literals","literal_inputs","expected_exception_class","exact_type_assertion"]
    result=[]
    for left,right in offsets:
        found=next((name for name in priority if any(name==kind and left<b and right>a for kind,a,b in regions)),None)
        if found: result.append(found)
        elif left>=start and right<=start+len(code): result.append("other_code_scaffolding")
        elif full[left:right]=="<|im_end|>": result.append("turn_end")
        else: result.append("mapping_or_prose")
    return result

def likelihood(model,tok,messages,code,ident):
    record=encode_answer(tok,messages,ident,16134)
    full=tok.apply_chat_template(messages,tokenize=False,enable_thinking=True,add_generation_prompt=False)
    encoded=tok(full,add_special_tokens=False,return_offsets_mapping=True)
    code_start=full.rfind(code); assert code_start>=0
    groups=token_groups(full,encoded["offset_mapping"],code,code_start)
    ids=torch.tensor([record["input_ids"]],device="cuda")
    labels=record["labels"]; first=record["first_target_token"]
    core=model.get_base_model()
    metrics=[]; seen=set()
    topk=TopKLogitsWarper(20); topp=TopPLogitsWarper(.95)
    with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
        hidden=core.model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False).last_hidden_state
        for start in range(0,len(labels)-1,32):
            end=min(start+32,len(labels)-1)
            if not any(v!=-100 for v in labels[start+1:end+1]): continue
            logits=core.lm_head(hidden[:,start:end,:])[0].float()
            target=torch.tensor(labels[start+1:end+1],device="cuda")
            active=target!=-100
            penalized=logits.clone()
            for local,position in enumerate(range(start,end)):
                if position>=first: seen.add(record["input_ids"][position])
                if seen: penalized[local,torch.tensor(sorted(seen),device="cuda")]-=1.5
            raw_loss=torch.nn.functional.cross_entropy(logits,target,ignore_index=-100,reduction="none")
            penalty_loss=torch.nn.functional.cross_entropy(penalized,target,ignore_index=-100,reduction="none")
            predictions=logits.argmax(-1); penalized_predictions=penalized.argmax(-1)
            gold_prob=torch.softmax(logits,dim=-1).gather(-1,target.clamp_min(0)[:,None]).squeeze(-1)
            dummy=torch.zeros((end-start,1),device="cuda",dtype=torch.long)
            filtered0=topp(dummy,topk(dummy,logits.clone()))
            filtered15=topp(dummy,topk(dummy,penalized.clone()))
            lp0=torch.log_softmax(filtered0,dim=-1).gather(-1,target.clamp_min(0)[:,None]).squeeze(-1)
            lp15=torch.log_softmax(filtered15,dim=-1).gather(-1,target.clamp_min(0)[:,None]).squeeze(-1)
            for j in range(end-start):
                position=start+j+1
                if labels[position]==-100: continue
                metrics.append({"position":position,"category":groups[position],"gold_id":labels[position],"predicted_id":int(predictions[j]),"penalized_predicted_id":int(penalized_predictions[j]),"raw_nll":raw_loss[j].item(),"presence15_nll":penalty_loss[j].item(),"raw_gold_probability":gold_prob[j].item(),"sample0_nll":-lp0[j].item() if torch.isfinite(lp0[j]) else None,"sample15_nll":-lp15[j].item() if torch.isfinite(lp15[j]) else None})
            del logits,penalized,target,raw_loss,penalty_loss,predictions,penalized_predictions,gold_prob,filtered0,filtered15,lp0,lp15
    def aggregate(rows):
        return {"tokens":len(rows),"raw_nll":sum(r["raw_nll"] for r in rows)/len(rows),"presence15_nll":sum(r["presence15_nll"] for r in rows)/len(rows),"raw_top1_accuracy":sum(r["gold_id"]==r["predicted_id"] for r in rows)/len(rows),"presence15_top1_accuracy":sum(r["gold_id"]==r["penalized_predicted_id"] for r in rows)/len(rows),"sample0_reference_tokens_excluded":sum(r["sample0_nll"] is None for r in rows),"sample15_reference_tokens_excluded":sum(r["sample15_nll"] is None for r in rows),"expected_different_draws_from_gold_raw_distribution":sum(1-r["raw_gold_probability"] for r in rows)}
    summary={"id":ident,"overall":aggregate(metrics),"by_category":{name:aggregate([r for r in metrics if r["category"]==name]) for name in sorted({r["category"] for r in metrics})},"interpretation":"Categories are approximate AST/source spans, not semantic correctness labels. A different token or literal may be a valid alternative. Target-excluded counts concern this one reference continuation, not all valid answers."}
    del ids,hidden
    torch.cuda.empty_cache()
    return summary,metrics

def main():
    p=argparse.ArgumentParser(); p.add_argument("--out",required=True); a=p.parse_args()
    out=(ROOT/a.out).resolve(); assert ROOT in out.parents and not out.exists(); out.mkdir(parents=True)
    plan={"status":"loading","models":["base","epoch-5"],"tasks":["DV001","DV002"],"new_decoders":["greedy-0","sample-0"],"reused_decoder":"sample-1.5 from qwenny-001-direct-001; same seed/prompt/runtime and unchanged weights","thinking":False,"max_new_tokens":2048,"context":16134,"seed":42,"sample_temperature":1.,"sample_top_k":20,"sample_top_p":.95,"repetition_penalty":1.,"training":"none","final_test":"never read","completed":[]}
    write(out/"report.json",plan); monitor=Monitor(out)
    try:
        shutil.copyfile(ROOT/"investigate_gap.py",out/"investigate_gap.py")
        shutil.copyfile(ROOT/"runtime.py",out/"runtime.py")
        tok=tokenizer(); model=PeftModel.from_pretrained(load_base(False),ROOT/"runs/qwenny-001/checkpoints/epoch-5",is_trainable=False)
        model.eval(); model.requires_grad_(False)
        old=ROOT/"probes/qwenny-001-direct-001"; corpus=EXP/"dataset-v1/candidate-006"
        likelihoods=[]
        for task in plan["tasks"]:
            messages=json.loads((old/task/"base-A/messages.json").read_text(encoding="utf-8"))
            assert messages==json.loads((old/task/"epoch-5-C/messages.json").read_text(encoding="utf-8"))
            target=(corpus/"tasks/development"/task/"TARGET.md").read_text(encoding="utf-8")
            code=(corpus/"tasks/development"/task/"test_target.py").read_text(encoding="utf-8")
            for variant in plan["models"]:
                plan.update(status="teacher-forcing",current_task=task,current_variant=variant); write(out/"report.json",plan)
                context=model.disable_adapter() if variant=="base" else contextlib.nullcontext()
                with context:
                    summary,metrics=likelihood(model,tok,messages+[{"role":"assistant","content":target}],code,task+"-"+variant)
                folder=out/"likelihood"/task/variant; folder.mkdir(parents=True)
                write(folder/"summary.json",summary); write(folder/"tokens.json",metrics)
                summary.update(task=task,variant=variant); likelihoods.append(summary)
                expected_file=ROOT/"runs/qwenny-001"/("base-development-loss.json" if variant=="base" else "epoch-5-development-loss.json")
                expected=next(r["loss"] for r in json.loads(expected_file.read_text()) if r["id"]==task+"-A")
                assert abs(summary["overall"]["raw_nll"]-expected)<.005,(task,variant,summary["overall"]["raw_nll"],expected)
        write(out/"likelihood-summary.json",likelihoods)
        variants=[("base-greedy-0","base",False),("epoch-5-greedy-0","epoch-5",False),("base-sample-0","base",True),("epoch-5-sample-0","epoch-5",True)]
        stops=[tok.convert_tokens_to_ids("<|im_end|>"),tok.convert_tokens_to_ids("<|endoftext|>")]
        for task_index,task in enumerate(plan["tasks"]):
            messages=json.loads((old/task/"base-A/messages.json").read_text(encoding="utf-8"))
            ordered=variants[task_index%4:]+variants[:task_index%4]
            for label,variant,sample in ordered:
                folder=out/task/label; folder.mkdir(parents=True); write(folder/"messages.json",messages)
                prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
                inputs=tok(prompt,return_tensors="pt",add_special_tokens=False).to("cuda")
                length=inputs["input_ids"].shape[1]
                assert length<16134
                torch.manual_seed(42); torch.cuda.manual_seed_all(42)
                kwargs={"do_sample":sample,"max_new_tokens":min(2048,16134-length),"repetition_penalty":1.,"use_cache":True,"eos_token_id":stops,"pad_token_id":tok.pad_token_id,"logits_processor":LogitsProcessorList([Progress(length,folder/"progress.json")])}
                if sample: kwargs.update(temperature=1.,top_k=20,top_p=.95)
                plan.update(status="generating",current_task=task,current_variant=label); write(out/"report.json",plan)
                context=model.disable_adapter() if variant=="base" else contextlib.nullcontext()
                start=time.monotonic()
                with context,torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                    generated=model.generate(**inputs,**kwargs)
                tail=generated[0,length:]; raw=tok.decode(tail,skip_special_tokens=False,clean_up_tokenization_spaces=False)
                terminated=int(tail[-1]) in stops
                (folder/"output.raw.txt").write_text(raw,encoding="utf-8")
                visible=raw.rsplit("</think>",1)[-1]
                for token in ("<|im_end|>","<|endoftext|>"): visible=visible.replace(token,"")
                (folder/"answer.md").write_text(visible,encoding="utf-8")
                fence=chr(96)*3; blocks=re.findall(fence+r"(?:python|py)?[ \t]*\n(.*?)"+fence,visible,re.S)
                if len(blocks)==1: (folder/"test_candidate.py").write_text(blocks[0],encoding="utf-8")
                item={"task":task,"variant":label,"decoder":"sample-0" if sample else "greedy-0","prompt_tokens":length,"generated_tokens":len(tail),"seconds":time.monotonic()-start,"terminated":terminated,"truncated":not terminated,"python_blocks":len(blocks),"memory":memory()}
                write(folder/"generation.json",item); plan["completed"].append(item); write(out/"report.json",plan)
                del inputs,generated,tail
                torch.cuda.empty_cache()
        plan["status"]="completed"; write(out/"report.json",plan)
    except BaseException as e:
        plan.update(status="failed",error=repr(e)); (out/"traceback.txt").write_text(traceback.format_exc(),encoding="utf-8"); write(out/"report.json",plan); raise
    finally: monitor.close()

if __name__=="__main__": main()
