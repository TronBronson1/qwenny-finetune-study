"""Preserve a stopped branch without substituting partial checkpoints for E5."""
import csv,pathlib,statistics
from prepare_study import HERE,EXP,read,rows,dump,sha
def main():
    execution=read(HERE/'execution-001.json')
    assert execution['status']=='stopped-failed-gate-or-budget'
    out=HERE/'stopped-evidence-001.json'; assert not out.exists()
    name='qwenny-003-calibrated-baseline'; run=EXP/'training-v1/runs'/name
    report=read(run/'report.json'); events=rows(run/'events.jsonl')
    batches=[r for r in events if r['kind']=='microbatch']
    zero=[r for r in batches if r['memory']['cuda_free']==0]
    positive=[r for r in batches if r['memory']['cuda_free']>0]
    windows=run/'windows-process-memory.csv'
    winrows=list(csv.DictReader(windows.open(encoding='utf-8-sig'))) if windows.exists() else []
    checkpoints=[]
    for epoch in (1,3,5):
        folder=run/'checkpoints'/f'epoch-{epoch}'
        if folder.exists():checkpoints.append(dict(epoch=epoch,files={p.name:sha(p) for p in folder.iterdir() if p.is_file()},fresh_import_status='not attempted; orchestration stopped before import/inference'))
    pre={arm:read(EXP/'training-v1/runs'/('s009-preflight-'+arm+'-001')/'report.json') for arm in ('baseline','comments')}
    assert all(r['status']=='preflight-passed' for r in pre.values())
    data=dict(status='stopped-no-paired-quality-comparison',execution=execution,baseline=dict(run=name,last_in_process_report_status=report['status'],in_process_status_note='Controller timeout is authoritative. Forced termination can leave the last child report showing training; no status was rewritten.',logged_completed_microbatches=len(batches),last_logged_optimizer_updates=batches[-1]['optimizer_updates'] if batches else 0,logged_input_tokens=sum(r['tokens'] for r in batches),logged_supervised_tokens=sum(r['target_tokens'] for r in batches),logged_microbatch_seconds=sum(r['seconds'] for r in batches),peak_allocated_bytes=max(r['memory']['peak_allocated'] for r in batches),peak_reserved_bytes=max(r['memory']['peak_reserved'] for r in batches),minimum_reported_cuda_free_bytes=min(r['memory']['cuda_free'] for r in batches),positive_free_samples=len(positive),zero_free_samples=len(zero),median_batch_seconds_positive_free=statistics.median(r['seconds'] for r in positive) if positive else None,median_batch_seconds_zero_free=statistics.median(r['seconds'] for r in zero) if zero else None,windows_process_memory_rows=len(winrows),checkpoints=checkpoints),comment_training='not started',preflights={arm:{k:r[k] for k in ('status','initial_adapter_sha256','masked_loss_validation','full_actual_example_preflight','generation_smoke')} for arm,r in pre.items()},inference=dict(planned=24,attempted=0,unattempted=24,reason='Training budget stop before E5 and before second arm; no generation launched'),quality_result='Not measured. All planned cells remain unattempted; do not interpret planned-denominator zeros as observed model incapability.',memory_interpretation='Timing slowdown coincides with reported CUDA-free memory reaching zero. Driver and allocator measures differ; available evidence does not identify another process, establish causal mechanism or prove shared-memory spill.',script_sha256=sha(pathlib.Path(__file__)))
    dump(out,data)
    dump(run/'TERMINATED_BY_CONTROLLER.json',dict(status='stopped-training-arm-wall-budget',execution_record=str(HERE/'execution-001.json'),last_logged_microbatches=len(batches),last_logged_updates=data['baseline']['last_logged_optimizer_updates'],endpoint='No E5; E1/E3 are incomplete-study artifacts and cannot replace frozen E5'))
if __name__=='__main__':main()
