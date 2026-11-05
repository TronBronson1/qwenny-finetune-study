"""Package compact-trial adapters separately; preserve all first-run packages."""
import collections,csv,datetime,hashlib,json,pathlib,shutil,statistics
ROOT=pathlib.Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    run=ROOT/'runs/qwenny-002-compact'; probe=ROOT/'probes/qwenny-002-compact-sample0-001'; out=ROOT/'candidates/qwenny-002-compact'
    report=json.loads((run/'report.json').read_text()); assert report['status']=='trained'
    generation=json.loads((probe/'report.json').read_text()); assert generation['status']=='completed'
    checks=json.loads((probe/'reload_checks.json').read_text()); assert len(checks)==3 and all(c['passed'] for c in checks)
    assert not out.exists(); out.mkdir(parents=True)
    events=[json.loads(line) for line in (run/'events.jsonl').read_text().splitlines()]
    batches=[e for e in events if e['kind']=='microbatch']; epochs=[e for e in events if e['kind']=='epoch-complete']
    counts=collections.Counter(e['id'] for e in batches)
    assert len(batches)==300 and len(counts)==60 and set(counts.values())=={5} and report['optimizer_updates']==75
    started=min(e['unix_time']-e['seconds'] for e in batches); ended=max(e['unix_time'] for e in batches)
    windows=list(csv.DictReader((run/'windows-process-memory.csv').open(encoding='utf-8-sig')))
    selected=[r for r in windows if started<=datetime.datetime.fromisoformat(r['timestamp_utc'].replace('Z','+00:00')).timestamp()<=ended]
    summary=dict(status='trained-and-import-verified',run='qwenny-002-compact',base=report['base'],revision=report['revision'],epochs=5,samples=300,distinct_tasks=60,optimizer_updates=75,elapsed_training_and_checkpoint_evaluation_seconds=report['elapsed_training_and_checkpoint_evaluation_seconds'],epoch_mean_training_losses={str(e['epoch']):e['mean_per_example_loss'] for e in epochs},training_peak_allocated_bytes=max(e['memory']['peak_allocated'] for e in batches),training_peak_reserved_bytes=max(e['memory']['peak_reserved'] for e in batches),min_stage_cuda_free_bytes=min(e['memory']['cuda_free'] for e in batches),windows_peak_shared_bytes=max(int(r['shared_bytes']) for r in selected),fresh_imports=checks,development_base=report['base_development_loss'],development_checkpoints=report['checkpoints'],target_token_reduction_fraction=report['preparation']['target_token_reduction_fraction'],comparison='Same examples, updates, base and numerical training runtime; fewer supervised tokens. Development targets unchanged. Compact train loss is not directly comparable to old-format train loss.',pilot_scope='Predeclared E5 only, two visible development families, sample0 seed42; see scoring folder for strict acceptance.',quality_claim='No general aptitude conclusion.')
    for epoch in (1,3,5):
        source=run/'checkpoints'/f'epoch-{epoch}'; target=out/f'Qwenny-Compact-E{epoch}'; target.mkdir()
        hashes={}
        for name in ('adapter_model.safetensors','adapter_config.json'):
            shutil.copyfile(source/name,target/name); assert sha(source/name)==sha(target/name); hashes[name]=sha(target/name)
        metadata=dict(name=f'Qwenny Compact E{epoch}',epoch=epoch,source_run=str(run),base=report['base'],base_revision=report['revision'],rank=4,alpha=8,trainable_parameters=report['trainable_parameters'],fresh_import=next(c for c in checks if c['epoch']==epoch),files=hashes,scope='Presentation-only target ablation on same 60 training tasks. Experimental PEFT adapter, not a standalone GGUF or verified aptitude level.')
        (target/'EXPERIMENT.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
        (target/'README.md').write_text(f'# Qwenny Compact E{epoch}\n\nExperimental PEFT adapter from compact-target trial qwenny-002-compact; same pinned base revision {report["revision"]}. Fresh import checked. See EXPERIMENT.json for hashes.\n\nUse the validated local NF4/BF16 runtime with frozen CPU input embedding. This is not a standalone LM Studio GGUF. No deployment or broad quality improvement is claimed.\n',encoding='utf-8')
    for name in ('COMPACT_TRIAL_PLAN.md','prepare_compact.py','validate_compact.py','compact_probe.py','package_compact.py'): shutil.copyfile(ROOT/name,run/name)
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (run/'training-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('development_checkpoints',)},indent=2))
if __name__=='__main__': main()
