"""Sequential GPU owner with hard wall ceilings; stop on any gate failure."""
import json,os,pathlib,subprocess,time,traceback
from prepare_study import HERE,EXP,read,dump,sha
from s009_bindings import verify_frozen
def main():
    verify_frozen(); report_path=HERE/'execution-001.json'; assert not report_path.exists()
    python=EXP/'lora-feasibility/.venv/Scripts/python.exe'
    started=time.monotonic(); deadline=started+10800
    report=dict(status='starting',process_id=os.getpid(),started_unix=time.time(),freeze_sha256=sha(HERE/'freeze-manifest.json'),jobs=[])
    def run(label,args,limit):
        remaining=deadline-time.monotonic(); assert remaining>0,'GPU orchestration budget exhausted'
        job=dict(label=label,status='running',start_unix=time.time(),maximum_seconds=min(remaining,limit)); report['jobs'].append(job); report['status']=label; dump(report_path,report)
        with (HERE/(label+'.log')).open('w',encoding='utf-8') as log:
            try:
                proc=subprocess.run([str(python)]+args,cwd=EXP,stdout=log,stderr=subprocess.STDOUT,timeout=min(remaining,limit))
                job.update(status='passed' if proc.returncode==0 else 'failed',exit_code=proc.returncode)
            except subprocess.TimeoutExpired:
                job.update(status='stopped-budget'); dump(report_path,report); raise
        job['seconds']=time.time()-job['start_unix']; dump(report_path,report)
        assert job['status']=='passed',(label,job)
    try:
        for arm in ('baseline','comments'):
            prepared=str(HERE/'preparation-001'/arm)
            run('preflight-'+arm,['studies/S009-value-comments/train_s009.py','--prepared',prepared,'--run','runs/s009-preflight-'+arm+'-001','--preflight-only'],600)
        pre=[read(EXP/'training-v1/runs'/('s009-preflight-'+a+'-001')/'report.json') for a in ('baseline','comments')]
        assert all(r['status']=='preflight-passed' for r in pre)
        assert pre[0]['initial_adapter_sha256']==pre[1]['initial_adapter_sha256']
        for arm,name in (('baseline','qwenny-003-calibrated-baseline'),('comments','qwenny-004-value-comments')):
            run('train-'+arm,['studies/S009-value-comments/train_s009.py','--prepared',str(HERE/'preparation-001'/arm),'--run','runs/'+name],1200)
        trained=[read(EXP/'training-v1/runs'/n/'report.json') for n in ('qwenny-003-calibrated-baseline','qwenny-004-value-comments')]
        for key in ('initial_adapter_sha256','initial_training_rng_sha256','initial_training_cuda_rng_sha256'):
            assert trained[0][key]==trained[1][key],key
        assert all(r['samples_seen']==300 and r['optimizer_updates']==75 for r in trained)
        report['paired_initial_state_and_updates']='matched'; dump(report_path,report)
        run('matched-inference',['studies/S009-value-comments/probe_s009.py'],min(7200,deadline-time.monotonic()))
        report['status']='gpu-work-completed-awaiting-source-review-and-scoring'
    except BaseException as e:
        report.update(status='stopped-failed-gate-or-budget',error=repr(e),traceback=traceback.format_exc()); raise
    finally:
        report['seconds']=time.monotonic()-started; dump(report_path,report)
if __name__=='__main__':main()
