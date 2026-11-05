"""Reuse bounded S007 gold execution engine on the exact S009 authored targets."""
import importlib.util,json,pathlib,sys,time
from prepare_study import HERE,EXP,DATA,read,rows,sha,dump,code,normalized,verify_inputs

def main():
    assert sys.version_info[:2]==(3,15)
    out=HERE/'validation-001'; assert not out.exists()
    verify_inputs()
    spec=importlib.util.spec_from_file_location('gold_engine',EXP/'studies/S007-measurement-repair/validate_repair_v2.py')
    engine=importlib.util.module_from_spec(spec); spec.loader.exec_module(engine); engine.OUT=out
    prep=HERE/'preparation-001'; authorization=read(prep/'authorization.json')
    manifest={r['id']:r for r in read(DATA/'manifest.json')['tasks']}
    jobs=[]
    for arm in ('baseline','comments'):
        packet=prep/arm/'messages.jsonl'
        assert sha(packet)==authorization['approved_export_hashes'][arm]
        records=rows(packet)
        for r in records:
            ident=r['id']; rec=manifest[ident]; assert rec['split']=='training'
            task=DATA/'tasks/training'/ident; source=code(r['messages'][-1]['content'])
            assert normalized(source)==normalized((task/'test_target.py').read_text(encoding='utf-8'))
            jobs.append((arm+'-'+ident,'reference',task/'evaluator/reference/subject.py',source,None,rec['function']))
            for m in read(task/'evaluator/mutants.json'):
                # TR058 fit overlay omitted pytest display IDs; bind its witness by
                # previously validated outcome vector instead of old gold node IDs.
                witness=m['witness']
                if ident=='TR058':
                    original=read(EXP/'studies/S007-measurement-repair/length-preview-002/validation.json')
                    assert original
                    # Runtime outcome-equivalence is separately retained below.
                    witness=None
                jobs.append((arm+'-'+ident,m['id'],task/'evaluator/mutants'/m['id']/'subject.py',source,witness,rec['function']))
    out.mkdir(); start=time.monotonic(); results=engine.run_jobs(jobs)
    # For TR058 compare every exact per-case outcome against the certified fit copy.
    import xml.etree.ElementTree as ET
    def vector(path):
        return [('skip' if t.find('skipped') is not None else 'error' if t.find('error') is not None else 'fail' if t.find('failure') is not None else 'pass') for t in ET.parse(path).findall('.//testcase')]
    for r in results:
        if r['task'].endswith('TR058') and r['variant']!='reference':
            prior=EXP/'studies/S007-measurement-repair/length-preview-002'
            # Locate execution XML by the variant's directory; fail if ambiguous.
            matches=[p for p in prior.rglob('*.xml') if r['variant'] in p.parts]
            assert len(matches)==1,(r['variant'],matches)
            current=out/r['task']/r['variant']/'report.xml'
            r['passed']=r['exit_code']==1 and vector(current)==vector(matches[0])
            r['evidence']='Exact per-case outcome vector matches certified fit overlay; no model node-name matching'
    failures=[r for r in results if not r['passed']]
    dump(out/'summary.json',dict(status='failed' if failures else 'passed',seconds=time.monotonic()-start,packet_hashes=authorization['approved_export_hashes'],references=sum(r['variant']=='reference' for r in results),mutants=sum(r['variant']!='reference' for r in results),failures=failures,results=results,script_sha256=sha(pathlib.Path(__file__))))
    print(json.dumps(dict(jobs=len(results),failures=len(failures)),indent=2))
    assert not failures
if __name__=='__main__': main()
