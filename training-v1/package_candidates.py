"""Package exact verified adapter copies; do not merge/requantize or modify the base."""
import argparse,collections,csv,datetime,hashlib,json,pathlib,shutil,statistics
ROOT=pathlib.Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(); p.add_argument("--run",required=True); p.add_argument("--probe",required=True); p.add_argument("--out",required=True); a=p.parse_args()
    run=ROOT/a.run; probe=ROOT/a.probe; out=ROOT/a.out
    assert not out.exists()
    report=json.loads((run/"report.json").read_text()); assert report["status"]=="trained"
    checks=json.loads((probe/"reload_checks.json").read_text()); assert len(checks)==3 and all(r["passed"] for r in checks)
    events=[json.loads(line) for line in (run/"events.jsonl").read_text().splitlines()]
    batches=[e for e in events if e["kind"]=="microbatch"]; epochs=[e for e in events if e["kind"]=="epoch-complete"]
    counts=collections.Counter(e["id"] for e in batches)
    assert len(batches)==300 and len(counts)==60 and set(counts.values())=={5}
    assert all(x.startswith("TR") for x in counts) and report["optimizer_updates"]==75
    start=min(e["unix_time"]-e["seconds"] for e in batches); end=max(e["unix_time"] for e in batches)
    windows=list(csv.DictReader((run/"windows-process-memory.csv").open(encoding="utf-8-sig")))
    training_windows=[r for r in windows if start<=datetime.datetime.fromisoformat(r["timestamp_utc"].replace("Z","+00:00")).timestamp()<=end]
    summary={"status":"trained-and-fresh-reload-verified","base":report["base"],"revision":report["revision"],"training_samples":300,"distinct_training_tasks":60,"optimizer_updates":75,"epochs":5,"elapsed_training_and_checkpoint_evaluation_seconds":report["elapsed_training_and_checkpoint_evaluation_seconds"],"epoch_mean_training_losses":{str(e["epoch"]):e["mean_per_example_loss"] for e in epochs},"median_microbatch_seconds":statistics.median(e["seconds"] for e in batches),"training_peak_allocated_bytes":max(e["memory"]["peak_allocated"] for e in batches),"training_peak_reserved_bytes":max(e["memory"]["peak_reserved"] for e in batches),"min_microbatch_stage_cuda_free_bytes":min(e["memory"]["cuda_free"] for e in batches),"windows_peak_process_shared_bytes_during_training_interval":max(int(r["shared_bytes"]) for r in training_windows),"reload_checks":checks,"development_base":report["base_development_loss"],"development_checkpoints":report["checkpoints"],"quality_claim":"None. Teacher-forced likelihood is not executable acceptance, regression safety or reasoning preservation. Final-test families are untouched by the model."}
    out.mkdir(parents=True)
    artifacts=[]
    for epoch in (1,3,5):
        source=run/"checkpoints"/f"epoch-{epoch}"; target=out/f"Qwenny-E{epoch}"; target.mkdir()
        hashes={}
        for name in ("adapter_config.json","adapter_model.safetensors"):
            shutil.copyfile(source/name,target/name); assert sha(source/name)==sha(target/name)
            hashes[name]=sha(target/name)
        checkpoint=next(c for c in report["checkpoints"] if c["epoch"]==epoch)
        metadata={"name":f"Qwenny E{epoch}","training_epochs":epoch,"same_trajectory":True,"base":report["base"],"base_revision":report["revision"],"rank":4,"alpha":8,"trainable_parameters":report["trainable_parameters"],"input_embedding":"Frozen BF16 CPU lookup; transformer/head/adapters CUDA","base_quantization":"NF4 with double quantization; BF16 compute","supervision":"Visible assistant answer and im_end only; prompt and empty thinking wrapper ignored","training_task_count":60,"samples_seen":checkpoint["samples_seen"],"optimizer_updates":checkpoint["optimizer_updates"],"development_teacher_forced_loss":checkpoint["development_loss"],"fresh_reload":next(r for r in checks if r["epoch"]==epoch),"source_checkpoint":str(source.resolve()),"files":hashes,"deployment":"PEFT adapter only, not a standalone GGUF. No LM Studio deployment/import has been verified."}
        (target/"EXPERIMENT.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
        (target/"README.md").write_text(f"# Qwenny E{epoch}\n\nVerified PEFT adapter after {epoch} training passes over 60 local tasks. Rank 4, alpha 8, seed 42; same trajectory as E1/E3/E5. Fresh import reproduced saved probe logits.\n\nUse the exact Qwen/Qwen3.5-9B base revision {report['revision']}. On the 3080 use the validated runtime.py layout: frozen input embedding in CPU RAM, NF4 base and chunked loss. This folder does not contain the base weights. The adapter config retains the original local base path; on another machine supply the exact base explicitly.\n\nDevelopment loss is recorded in EXPERIMENT.json. No broad quality/aptitude or thinking-mode preservation claim is made. This is not a standalone LM Studio GGUF; export/import and matched deployment checks are separate.\n",encoding="utf-8")
        artifacts.append(metadata)
    summary["candidates"]=artifacts
    (out/"SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    (ROOT/"training-summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("development_checkpoints","candidates")},indent=2))

if __name__=="__main__": main()
