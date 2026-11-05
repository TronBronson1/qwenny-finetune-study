"""Prospective scorer checks on eight gold suites, renamed nodes and bad controls."""
import json,pathlib,sys,time
from prepare_study import HERE,DATA,read,dump,sha
from suite_scorer import score
IDS=('TR024','DV008','TR025','DV004','TR038','DV011','TR049','DV007')
def main():
    out=HERE/'scorer-calibration-001'; assert not out.exists(); out.mkdir()
    records=[]; start=time.monotonic()
    for ident in IDS:
        task=DATA/'tasks'/('training' if ident.startswith('TR') else 'development')/ident
        # Deliberately rename all test nodes to prove no dependence on gold names.
        source=out/(ident+'.py')
        source.write_text((task/'test_target.py').read_text(encoding='utf-8').replace('def test_','def test_renamed_'),encoding='utf-8')
        review=dict(source_sha256=sha(source),approved_for_isolated_execution=True,meaningful_contract_assertions=True,basis='S007 calibrated gold plus agent inspection; node names changed only. No independent review claimed.')
        result=score(source,task,out/ident,sys.executable,review)
        passed=result['reference_valid'] and result['eligible_candidate_mutants']==result['designated_mutants']
        records.append(dict(task=ident,passed=passed,reference_valid=result['reference_valid'],witnessed=result['eligible_candidate_mutants'],mutants=result['designated_mutants']))
        print(json.dumps(records[-1]),flush=True)
    task=DATA/'tasks/training/TR049'
    controls={
        'empty':'',
        'pass-only':'def test_noop(): pass\n',
        'vacuous-call':'from subject import row_major_offset\ndef test_noop():\n row_major_offset(0,0,1,1)\n assert True\n',
        'skip-only':"import pytest\nfrom subject import row_major_offset\n@pytest.mark.skip(reason='control')\ndef test_skip(): assert row_major_offset(0,0,1,1)==0\n",
        'reference-invalid':'from subject import row_major_offset\ndef test_wrong(): assert row_major_offset(0,0,1,1)==999\n',
    }
    negative=[]
    for name,text in controls.items():
        source=out/(name+'.py'); source.write_text(text,encoding='utf-8')
        result=score(source,task,out/name,sys.executable,dict(source_sha256=sha(source),approved_for_isolated_execution=True,meaningful_contract_assertions=name=='reference-invalid',basis='Explicit scorer negative control'))
        negative.append(dict(control=name,passed=not result['reference_valid'] and result['eligible_candidate_mutants'] is None))
    # Unit-test the eligibility boundary through the real subprocess tracer using
    # a trusted temporary fixture copy, never modifying the calibrated dataset.
    import shutil
    fixture=out/'training'/'CRASH'; shutil.copytree(task,fixture)
    (fixture/'evaluator/mutants/M01/subject.py').write_text("def row_major_offset(*args): raise RuntimeError('unrelated valid-input crash')\n",encoding='utf-8')
    dump(fixture/'evaluator/mutants.json',[dict(id='M01')])
    source=out/'unrelated-crash.py'; source.write_text('from subject import row_major_offset\ndef test_value(): assert row_major_offset(0,0,1,1)==0\n',encoding='utf-8')
    r=score(source,fixture,out/'unrelated-crash',sys.executable,dict(source_sha256=sha(source),approved_for_isolated_execution=True,meaningful_contract_assertions=True,basis='Trusted calibration control'))
    negative.append(dict(control='unrelated-valid-input-crash',passed=r['reference_valid'] and r['eligible_candidate_mutants']==0))
    status='passed' if all(r['passed'] for r in records+negative) else 'failed'
    dump(out/'summary.json',dict(status=status,gold=records,negative=negative,seconds=time.monotonic()-start,scorer_sha256=sha(HERE/'suite_scorer.py'),plugin_sha256=sha(HERE/'trace_plugin.py'),limitation='Finite gold/negative calibration; arbitrary model coverage and evidence still require explicit hash-bound semantic review'))
    assert status=='passed'
if __name__=='__main__': main()
