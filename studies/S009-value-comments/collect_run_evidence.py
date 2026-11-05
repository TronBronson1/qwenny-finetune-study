"""Audit observed paired trajectories/costs without using loss to choose endpoints."""
import csv,json,pathlib
from prepare_study import HERE,EXP,read,rows,dump,sha
def main():
    out=HERE/'run-evidence-001.json'; assert not out.exists()
    reports={}; orders={}
    for arm,name in (('baseline','qwenny-003-calibrated-baseline'),('comments','qwenny-004-value-comments')):
        root=EXP/'training-v1/runs'/name; report=read(root/'report.json'); assert report['status']=='trained'
        events=rows(root/'events.jsonl'); batches=[r for r in events if r['kind']=='microbatch']
        assert len(batches)==300 and {r['id'] for r in batches}=={f'TR{i:03}' for i in range(1,61)}
        assert report['optimizer_updates']==75
        assert all(sum(r['id']==ident for r in batches)==5 for ident in {r['id'] for r in batches})
        orders[arm]=[(r['epoch'],r['position'],r['id'],r['optimizer_updates']) for r in batches]
        observed=dict(microbatches=len(batches),updates=report['optimizer_updates'],input_tokens=sum(r['tokens'] for r in batches),supervised_tokens=sum(r['target_tokens'] for r in batches),microbatch_seconds=sum(r['seconds'] for r in batches),training_and_checkpoint_eval_seconds=report['elapsed_training_and_checkpoint_evaluation_seconds'],peak_allocated_bytes=max(r['memory']['peak_allocated'] for r in batches),peak_reserved_bytes=max(r['memory']['peak_reserved'] for r in batches),minimum_cuda_free_bytes=min(r['memory']['cuda_free'] for r in batches))
        path=root/'windows-process-memory.csv'
        memory_rows=list(csv.DictReader(path.open(encoding='utf-8-sig'))) if path.exists() else []
        observed['windows_process_memory_rows']=len(memory_rows)
        observed['windows_process_memory_note']='Retain raw sampler output; absent/incomplete data does not establish shared-memory spill.'
        observed['initial_adapter_sha256']=report['initial_adapter_sha256']; observed['initial_training_rng_sha256']=report['initial_training_rng_sha256']; observed['initial_training_cuda_rng_sha256']=report['initial_training_cuda_rng_sha256']
        observed['epoch_mean_training_losses']={str(r['epoch']):r['mean_per_example_loss'] for r in events if r['kind']=='epoch-complete'}
        observed['checkpoint_adapter_hashes']={str(e):sha(root/'checkpoints'/f'epoch-{e}'/'adapter_model.safetensors') for e in (1,3,5)}
        reports[arm]=observed
    assert orders['baseline']==orders['comments']
    for key in ('initial_adapter_sha256','initial_training_rng_sha256','initial_training_cuda_rng_sha256'):
        assert reports['baseline'][key]==reports['comments'][key]
    generation=read(HERE/'inference-001/report.json')
    reload=read(HERE/'inference-001/reload_checks.json')
    assert len(reload)==6 and all(r['passed'] and r['max_abs_logit_difference']==0 for r in reload)
    data=dict(status='observed-evidence-verified',paired_same_initial_adapter_rng_and_shuffle=True,training=reports,import_checks=reload,inference=dict(status=generation['status'],attempts=len(generation['completed']),unattempted=generation.get('unattempted',[]),elapsed_seconds=generation['elapsed_seconds'],generation_seconds=sum(r['seconds'] for r in generation['completed']),output_tokens=sum(r['generated_tokens'] for r in generation['completed']),terminated=sum(r['terminated'] for r in generation['completed'])),gpu_orchestration=read(HERE/'execution-001.json'),quality_claim='None from loss; E5 remains the frozen endpoint.',script_sha256=sha(pathlib.Path(__file__)))
    dump(out,data)
if __name__=='__main__':main()
