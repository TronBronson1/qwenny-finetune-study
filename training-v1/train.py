"""Controlled 1/3/5-epoch local LoRA trajectory; final-test records are never read."""
import argparse, gc, hashlib, importlib.metadata, json, math, os, pathlib, random, shutil, statistics, subprocess, sys, time, traceback
import torch
from runtime import ROOT,EXP,BASE,REV,load_base,attach_lora,tokenizer,tensors,masked_loss,memory,Monitor,verify_checkpoint

def write(path,value): path.write_text(json.dumps(value,indent=2),encoding="utf-8")
def read_rows(path): return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

def main():
    p=argparse.ArgumentParser(); p.add_argument("--prepared",default="prepared-001"); p.add_argument("--run",required=True); a=p.parse_args()
    out=(ROOT/a.run).resolve()
    assert ROOT in out.parents and not out.exists()
    out.mkdir(parents=True)
    report={"status":"starting","base":BASE,"revision":REV,"process_id":os.getpid(),"seed":42,"epochs":5,"candidate_epochs":[1,3,5],"batch_size":1,"gradient_accumulation":4,"rank":4,"alpha":8,"loss_chunk":128,"learning_rate":1e-4,"warmup_optimizer_updates":3,"weight_decay":.01,"gradient_clip":1.0,"layout":"frozen BF16 input embedding on CPU; rest on CUDA; NF4 frozen linear base","reasoning_policy":"Direct visible assistant targets plus im_end only; prompt, roles and empty thinking wrapper masked. Historical LM Studio settings unchanged.","samples_seen":0,"optimizer_updates":0}
    def save(): write(out/"report.json",report)
    def event(kind,**details):
        item=dict(kind=kind,unix_time=time.time(),**details)
        with (out/"events.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps(item)+"\n")
    save(); monitor=Monitor(out)
    try:
        prepared=ROOT/a.prepared
        preparation=json.loads((prepared/"report.json").read_text())
        for name in ("train","development"):
            assert hashlib.sha256((prepared/(name+".jsonl")).read_bytes()).hexdigest()==preparation[name+"_jsonl_sha256"]
        train=read_rows(prepared/"train.jsonl"); dev=read_rows(prepared/"development.jsonl")
        assert len(train)==60 and len(dev)==24 and max(r["input_tokens"] for r in train)<=2048
        assert all(r["id"].startswith("TR") for r in train) and all(r["task_id"].startswith("DV") for r in dev)
        report["preparation"]=preparation
        report["packages"]={name:importlib.metadata.version(name) for name in ["torch","transformers","peft","accelerate","bitsandbytes"]}
        for name in ["runtime.py","train.py","prepare_data.py"]:
            shutil.copyfile(ROOT/name,out/name)
        shutil.copyfile(prepared/"report.json",out/"data-preparation.json")
        subprocess.run([sys.executable,"-m","pip","freeze"],stdout=(out/"packages.lock.txt").open("w"),check=True)
        report["status"]="verifying-checkpoint"; save()
        verify_checkpoint()
        random.seed(42); torch.manual_seed(42); torch.cuda.manual_seed_all(42)
        report["status"]="loading"; save()
        model,parameters,targets=attach_lora(load_base(training=True)); tok=tokenizer()
        report["target_modules"]=targets; report["trainable_parameters"]=sum(p.numel() for p in parameters.values())
        assert model.get_input_embeddings().weight.device.type=="cpu"
        assert model.get_output_embeddings().weight.device.type=="cuda"
        report["memory_after_load"]=memory()
        # Check labels with a mixed masked/supervised window, not a synthetic all-token objective.
        longest=max(train,key=lambda r:r["input_tokens"])
        ids,attention,labels=tensors(longest)
        first=longest["first_target_token"]; left=max(0,first-32); right=min(ids.shape[1],left+64)
        probe,probe_attention,probe_labels=ids[:,left:right],attention[:,left:right],labels[:,left:right]
        assert (probe_labels==-100).any() and (probe_labels!=-100).any()
        model.train()
        with torch.autocast("cuda",dtype=torch.bfloat16):
            standard=model(input_ids=probe,attention_mask=probe_attention,labels=probe_labels,use_cache=False).loss
        standard.backward()
        reference={n:p.grad.detach().float().cpu().clone() for n,p in parameters.items() if p.grad is not None}
        value=standard.item(); model.zero_grad(set_to_none=True)
        with torch.autocast("cuda",dtype=torch.bfloat16): checked=masked_loss(model,probe,probe_attention,probe_labels,32)
        checked.backward()
        norm=sum(g.square().sum().item() for g in reference.values())**.5
        diff=sum((p.grad.detach().float().cpu()-reference[n]).square().sum().item() for n,p in parameters.items() if n in reference)**.5
        report["masked_loss_validation"]={"record":longest["id"],"window_tokens":right-left,"standard":value,"chunked":checked.item(),"gradient_relative_l2_difference":diff/max(norm,1e-12)}
        assert abs(value-checked.item())<1e-3 and diff/max(norm,1e-12)<.03
        model.zero_grad(set_to_none=True)
        del standard,checked,reference,probe,probe_attention,probe_labels
        gc.collect(); torch.cuda.empty_cache()
        with torch.autocast("cuda",dtype=torch.bfloat16): full_loss=masked_loss(model,ids,attention,labels)
        full_loss.backward()
        assert torch.isfinite(full_loss) and all(p.grad is None or torch.isfinite(p.grad).all().item() for p in parameters.values())
        assert all(p.grad is None for n,p in model.named_parameters() if n not in parameters)
        report["full_actual_example_preflight"]={"id":longest["id"],"input_tokens":ids.shape[1],"target_tokens":longest["target_tokens"],"loss":full_loss.item(),"memory":memory()}
        model.zero_grad(set_to_none=True)
        del ids,attention,labels,full_loss
        gc.collect(); torch.cuda.empty_cache()
        # A short direct-answer cached-generation smoke test, not a scored development answer.
        model.eval()
        prompt=tok.apply_chat_template([{"role":"user","content":"Reply with only the word blue."}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
        batch=tok(prompt,return_tensors="pt",add_special_tokens=False).to("cuda")
        stops=[tok.convert_tokens_to_ids("<|im_end|>"),tok.convert_tokens_to_ids("<|endoftext|>")]
        with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16):
            generated=model.generate(**batch,max_new_tokens=24,do_sample=False,use_cache=True,eos_token_id=stops,pad_token_id=tok.pad_token_id)
        tail=generated[0,batch["input_ids"].shape[1]:]
        report["generation_smoke"]={"tokens":len(tail),"text":tok.decode(tail,skip_special_tokens=False),"terminated":int(tail[-1]) in stops}
        assert len(tail)>0 and int(tail[-1]) in stops,"Cached generation did not terminate in smoke check"
        del batch,generated,tail
        gc.collect(); torch.cuda.empty_cache()
        report["status"]="base-development-controls"; save()
        def dev_losses(label):
            model.eval(); rows=[]
            for record in dev:
                ids,attention,labels=tensors(record)
                with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16): loss=masked_loss(model,ids,attention,labels)
                assert torch.isfinite(loss)
                rows.append({"id":record["id"],"task_id":record["task_id"],"arm":record["arm"],"tokens":record["input_tokens"],"target_tokens":record["target_tokens"],"loss":loss.item()})
                del ids,attention,labels,loss
            write(out/(label+"-development-loss.json"),rows)
            aggregate={arm:statistics.mean(r["loss"] for r in rows if r["arm"]==arm) for arm in ["A","B"]}
            event("development-loss",label=label,mean_per_example=aggregate)
            return aggregate
        with model.disable_adapter(): report["base_development_loss"]=dev_losses("base")
        report["preflight"]="passed"; report["status"]="training"; save()
        torch.cuda.reset_peak_memory_stats()
        optimizer=torch.optim.AdamW(parameters.values(),lr=1e-4,betas=(.9,.999),eps=1e-8,weight_decay=.01)
        optimizer.zero_grad(set_to_none=True)
        start_run=time.monotonic()
        for epoch in range(1,6):
            order=list(range(len(train))); random.Random(42+epoch).shuffle(order)
            losses=[]; model.train()
            for position,index in enumerate(order,1):
                record=train[index]
                report.update(status="training",epoch=epoch,position=position,task=record["id"]); save()
                tick=time.monotonic(); ids,attention,labels=tensors(record)
                with torch.autocast("cuda",dtype=torch.bfloat16): loss=masked_loss(model,ids,attention,labels)
                assert torch.isfinite(loss)
                raw=loss.item(); (loss/4).backward()
                losses.append(raw); report["samples_seen"]+=1
                if position%4==0:
                    assert all(p.grad is None for n,p in model.named_parameters() if n not in parameters)
                    grads=[p.grad for p in parameters.values() if p.grad is not None]
                    assert grads and all(torch.isfinite(g).all().item() for g in grads)
                    assert any(torch.count_nonzero(g).item()>0 for g in grads)
                    before={n:p.detach().cpu().clone() for n,p in parameters.items()}
                    torch.nn.utils.clip_grad_norm_(list(parameters.values()),1.0,error_if_nonfinite=True)
                    update=report["optimizer_updates"]+1
                    lr=1e-4*min(1.,update/3)
                    for group in optimizer.param_groups: group["lr"]=lr
                    optimizer.step(); optimizer.zero_grad(set_to_none=True)
                    assert any(not torch.equal(before[n],p.detach().cpu()) for n,p in parameters.items())
                    report["optimizer_updates"]=update
                    del before,grads
                event("microbatch",epoch=epoch,position=position,id=record["id"],tokens=record["input_tokens"],target_tokens=record["target_tokens"],loss=raw,seconds=time.monotonic()-tick,optimizer_updates=report["optimizer_updates"],memory=memory())
                del ids,attention,labels,loss
            event("epoch-complete",epoch=epoch,mean_per_example_loss=statistics.mean(losses),samples_seen=report["samples_seen"],optimizer_updates=report["optimizer_updates"])
            if epoch in (1,3,5):
                folder=out/"checkpoints"/f"epoch-{epoch}"; folder.mkdir(parents=True)
                model.save_pretrained(folder,safe_serialization=True)
                torch.save({"epoch":epoch,"optimizer":optimizer.state_dict(),"torch_rng":torch.get_rng_state(),"cuda_rng":torch.cuda.get_rng_state_all(),"python_rng":random.getstate(),"dataset_order_seed":42+epoch},folder/"training-state.pt")
                model.eval()
                probe=torch.tensor([train[0]["input_ids"][:32]],device="cuda")
                with torch.no_grad(),torch.autocast("cuda",dtype=torch.bfloat16): logits=model(input_ids=probe,use_cache=False,logits_to_keep=1).logits.float().cpu()
                torch.save({"input_ids":probe.cpu(),"logits":logits},folder/"reload-probe.pt")
                del probe,logits
                report.setdefault("checkpoints",[]).append({"epoch":epoch,"path":str(folder),"samples_seen":report["samples_seen"],"optimizer_updates":report["optimizer_updates"],"development_loss":dev_losses(f"epoch-{epoch}")})
                event("checkpoint-saved",epoch=epoch,path=str(folder)); save()
            model.train()
        report.update(status="trained",elapsed_training_and_checkpoint_evaluation_seconds=time.monotonic()-start_run,memory=memory(),quality_claim="None. Development teacher-forced loss is not strict task acceptance or reasoning/regression preservation.")
        save()
    except BaseException as e:
        report["status"]="interrupted" if isinstance(e,KeyboardInterrupt) else "failed"; report["error"]=repr(e)
        (out/"traceback.txt").write_text(traceback.format_exc(),encoding="utf-8"); save(); raise
    finally:
        monitor.close(); save()

if __name__=="__main__": main()
