"""Read-only numerical diagnostic: cached decoding versus full-context forward passes."""
import argparse,contextlib,json,pathlib,time,traceback
import torch
from peft import PeftModel
from runtime import ROOT,load_base,tokenizer,Monitor

def main():
    p=argparse.ArgumentParser(); p.add_argument("--training-run",required=True); p.add_argument("--probe",required=True); p.add_argument("--out",required=True); a=p.parse_args()
    out=ROOT/a.out; assert not out.exists(); out.mkdir(parents=True)
    report={"status":"loading","scope":"Numerical diagnostic only, not extra scored task samples or training.","results":[]}
    def save(): (out/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    save(); monitor=Monitor(out)
    try:
        tok=tokenizer(); model=PeftModel.from_pretrained(load_base(False),ROOT/a.training_run/"checkpoints"/"epoch-5",is_trainable=False)
        model.eval(); model.requires_grad_(False)
        messages=json.loads((ROOT/a.probe/"DV001"/"base-A"/"messages.json").read_text(encoding="utf-8"))
        prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
        inputs=tok(prompt,return_tensors="pt",add_special_tokens=False).to("cuda")
        length=inputs["input_ids"].shape[1]; stops=[tok.convert_tokens_to_ids("<|im_end|>"),tok.convert_tokens_to_ids("<|endoftext|>")]
        for label in ("base","epoch-5"):
            context=model.disable_adapter() if label=="base" else contextlib.nullcontext()
            rows=[]; report.update(status="checking",current_variant=label); save()
            with context,torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
                generated=model.generate(**inputs,do_sample=False,max_new_tokens=16,use_cache=True,return_dict_in_generate=True,output_logits=True,eos_token_id=stops,pad_token_id=tok.pad_token_id)
                for step in [0,1,3,7,15]:
                    if step>=len(generated.logits): continue
                    prefix=generated.sequences[:,:length+step]
                    complete=model(input_ids=prefix,use_cache=False,logits_to_keep=1).logits[0,-1,:].float()
                    cached=generated.logits[step][0].float()
                    delta=(complete-cached).abs()
                    p_log=torch.log_softmax(complete,dim=-1); q_log=torch.log_softmax(cached,dim=-1)
                    kl=(p_log.exp()*(p_log-q_log)).sum().item()
                    rows.append({"step":step,"max_abs_difference":delta.max().item(),"mean_abs_difference":delta.mean().item(),"kl_full_to_cached":kl,"argmax_matches":int(complete.argmax())==int(cached.argmax())})
                    del complete,cached,delta,p_log,q_log
            report["results"].append({"variant":label,"rows":rows,"greedy_diagnostic_generated_tokens":generated.sequences.shape[1]-length,"interpretation":"BF16/full-matrix versus incremental paths need not be bit-identical; inspect divergence rather than assume a cache bug."})
            del generated
        report["status"]="completed"; save()
    except BaseException as e:
        report.update(status="failed",error=repr(e)); (out/"traceback.txt").write_text(traceback.format_exc(),encoding="utf-8"); save(); raise
    finally: monitor.close()

if __name__=="__main__": main()
