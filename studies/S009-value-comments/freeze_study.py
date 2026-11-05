"""Freeze complete source/input bindings only after all CPU gates pass."""
import pathlib,sys
from prepare_study import HERE,EXP,DATA,verify_inputs,read,sha,dump
def main():
    assert not (HERE/'freeze-manifest.json').exists()
    verify_inputs()
    for gate in ('validation-001/summary.json','scorer-calibration-001/summary.json','guard-checks.json'):
        assert read(HERE/gate)['status']=='passed',gate
    # Safety/semantic review of selected gold is inherited from S007 rubric repair;
    # runtime scorer calibration uses the identical contract requirements.
    gold=[]
    for row in read(HERE/'selection.json')['tasks']:
        task=DATA/'tasks'/row['split']/row['id']; rubric=read(task/'rubric.json')
        gold.append(dict(task=row['id'],source_sha256=sha(task/'test_target.py'),rubric_sha256=sha(task/'rubric.json'),semantic_categories=rubric['semantic_categories'],requirement_review='S007 task-specific gold/category mapping, type/order/nonmutation review plus current eight-gold executable fixture calibration; same-agent, no independent sign-off',strict_calibrated_acceptance=True))
    dump(HERE/'gold-rubric-review.json',dict(records=gold,review_limit='Finite explicit rubric and designated fixtures; not exhaustive semantic proof'))
    files={}
    paths=list(HERE.glob('*.py'))+[HERE/'PROTOCOL.md',HERE/'selection.json',HERE/'guard-checks.json',HERE/'gold-rubric-review.json',HERE/'validation-001/summary.json',HERE/'scorer-calibration-001/summary.json']
    paths+=list((HERE/'preparation-001').rglob('*'))+list((HERE/'inputs').rglob('*'))
    paths += [EXP/'training-v1'/n for n in ('runtime.py','prepare_data.py','score_s006.py')]
    paths += [DATA/'SHA256.json']+[DATA/name for name in read(DATA/'SHA256.json')]
    for path in paths:
        if path.is_file():files[path.relative_to(EXP).as_posix()]=sha(path)
    dump(HERE/'freeze-manifest.json',dict(study='S009',status='frozen-before-new-GPU-work',files=files,authorization='User explicitly approved proceeding with the handoff plan; exact new packet hashes bound in preparation authorization; no fabricated exact-text user review',endpoint='E5 only',maximum_gpu_orchestration_seconds=10800))
    print('Frozen files:',len(files))
if __name__=='__main__':main()
