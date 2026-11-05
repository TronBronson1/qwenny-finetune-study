"""Reference validity plus input-bound mutant evidence; semantic review stays explicit."""
import argparse,ast,json,os,pathlib,shutil,subprocess,sys,time,xml.etree.ElementTree as ET
from prepare_study import HERE,EXP,DATA,read,sha,dump
sys.path.insert(0,str(EXP/'training-v1'))
from score_s006 import inspect_ast

def execute(source,task,variant,out,python):
    fixture=task/'evaluator'
    work=out/variant; work.mkdir(parents=True)
    shutil.copyfile(source,work/'test_candidate.py')
    shutil.copyfile(fixture/('reference' if variant=='reference' else 'mutants/'+variant)/'subject.py',work/'subject.py')
    shutil.copyfile(HERE/'trace_plugin.py',work/'conftest.py')
    record=read(task/'record.json')
    dump(work/'trace-config.json',dict(reference=str(fixture/'reference/subject.py'),function=record['function']))
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
    tick=time.monotonic()
    try:
        process=subprocess.run([python,'-m','pytest','-q','-p','no:cacheprovider','--junitxml=report.xml','test_candidate.py'],cwd=work,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
        status=process.returncode; log=process.stdout+process.stderr
    except subprocess.TimeoutExpired:
        status='timeout'; log='Infrastructure/time budget stop; ineligible for mutant credit.'
    (work/'pytest.log').write_text(log,encoding='utf-8')
    tests=ET.parse(work/'report.xml').findall('.//testcase') if (work/'report.xml').exists() else []
    calls=read(work/'calls.json') if (work/'calls.json').exists() else []
    # Node names bind executions only within this generated suite, never to gold IDs.
    candidates=[]
    for test in tests:
        failure=test.find('failure')
        if failure is None: continue
        text=(failure.text or '')+' '+failure.attrib.get('message','')
        for call in calls:
            if not call['node'] or call['node'].split('::')[-1]!=test.attrib.get('name'): continue
            expected,actual=call['expected'],call['actual']
            mismatch=expected!=actual or call['expected_after']!=call['actual_after']
            kind=None
            if 'exception' not in expected and 'exception' not in actual and mismatch and ('AssertionError' in text or failure.attrib.get('message','').startswith('assert')):
                kind='result-or-post-state-assertion'
            elif expected.get('exception') in ('TypeError','ValueError','IndexError'):
                if 'exception' not in actual and 'DID NOT RAISE' in text: kind='required-exception-not-raised'
                elif actual.get('exception') in ('TypeError','ValueError','IndexError') and actual!=expected and failure.attrib.get('message','').startswith(actual['exception']+':'):
                    kind='required-exception-wrong-class'
            if kind:
                candidates.append(dict(kind=kind,test=test.attrib.get('name'),call=call,review_status='requires source/contract review; finite input-bound evidence only'))
    valid=status==0 and bool(tests) and bool(calls) and not any(t.find(k) is not None for t in tests for k in ('failure','error','skipped'))
    return dict(variant=variant,exit_code=status,test_cases=len(tests),calls=len(calls),reference_valid=valid,candidate_witnesses=candidates,seconds=time.monotonic()-tick,source_sha256=sha(source),trace_sha256=sha(work/'calls.json') if (work/'calls.json').exists() else None)

def score(source,task,out,python,review):
    assert review['source_sha256']==sha(source) and review['approved_for_isolated_execution'] is True,'Hash-bound source inspection required'
    assert task.parent.name in ('training','development')
    inspect_ast(source.read_text(encoding='utf-8'),read(task/'record.json')['function'])
    out.mkdir(parents=True)
    variants=['reference']+[m['id'] for m in read(task/'evaluator/mutants.json')]
    results=[execute(source,task,v,out,python) for v in variants]
    valid=results[0]['reference_valid'] and review.get('meaningful_contract_assertions') is True
    summary=dict(source_sha256=sha(source),review=review,reference_valid=valid,variants=results,designated_mutants=len(variants)-1,eligible_candidate_mutants=sum(bool(r['candidate_witnesses']) for r in results[1:]) if valid else None,strict_acceptance='pending hash-bound requirement/prose and witness review',policy='No mutant credit for reference-invalid suites. Node names bind actual generated calls only. Valid-input crashes are ineligible. Related validation-class mismatches only on reference-invalid inputs. Trace candidates require semantic review before final credit.')
    dump(out/'summary.json',summary); return summary

def main():
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--task',required=True); p.add_argument('--review',required=True); p.add_argument('--out',required=True); p.add_argument('--python',required=True); a=p.parse_args()
    score(pathlib.Path(a.source),pathlib.Path(a.task),pathlib.Path(a.out),a.python,read(pathlib.Path(a.review)))
if __name__=='__main__': main()
