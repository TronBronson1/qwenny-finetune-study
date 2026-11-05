"""Compare original and compact pytest outcomes on unchanged training fixtures."""
import argparse,collections,concurrent.futures,hashlib,json,os,pathlib,shutil,subprocess,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser(); p.add_argument('--prepared',default='prepared-compact-001'); p.add_argument('--out',default='validation-compact-001'); p.add_argument('--python',required=True); a=p.parse_args()
    prepared=ROOT/a.prepared; out=ROOT/a.out; assert not out.exists(); out.mkdir()
    data=json.loads((prepared/'report.json').read_text()); jobs=[]
    for row in data['per_task']:
        ident=row['id']; original=ROOT.parent/'dataset-v1/candidate-006/tasks/training'/ident
        variants=[('reference',original/'evaluator/reference/subject.py')]+[(m['id'],original/'evaluator/mutants'/m['id']/'subject.py') for m in json.loads((original/'evaluator/mutants.json').read_text())]
        assert hashlib.sha256((original/'test_target.py').read_text(encoding='utf-8').encode()).hexdigest()==row['original_code_sha256']
        for label,subject in variants:
            for form,code in [('original',original/'test_target.py'),('compact',prepared/'targets'/ident/'test_target.py')]: jobs.append((ident,label,subject,form,code))
    def run(job):
        ident,label,subject,form,code=job; work=out/ident/label/form; work.mkdir(parents=True)
        shutil.copyfile(subject,work/'subject.py'); shutil.copyfile(code,work/'test_target.py')
        env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
        result=subprocess.run([a.python,'-m','pytest','-q','-p','no:cacheprovider','--junitxml=report.xml','test_target.py'],cwd=work,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=30)
        (work/'pytest.log').write_text(result.stdout+result.stderr,encoding='utf-8')
        counts=collections.Counter()
        for test in ET.parse(work/'report.xml').findall('.//testcase'):
            outcome='failure' if test.find('failure') is not None else 'error' if test.find('error') is not None else 'skipped' if test.find('skipped') is not None else 'passed'
            counts[test.attrib.get('classname','')+'::'+test.attrib.get('name','').split('[')[0]+'::'+outcome]+=1
        return dict(task=ident,variant=label,form=form,exit_code=result.returncode,outcomes=dict(counts))
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for row in pool.map(run,jobs):
            rows.append(row)
            if len(rows)%40==0: (out/'progress.json').write_text(json.dumps(dict(completed=len(rows),total=len(jobs))))
    pairs={}
    for row in rows: pairs.setdefault((row['task'],row['variant']),{})[row['form']]=row
    equal=all(v['original']['exit_code']==v['compact']['exit_code'] and v['original']['outcomes']==v['compact']['outcomes'] for v in pairs.values())
    refs=[r for r in rows if r['variant']=='reference' and r['form']=='compact']
    mutants=[r for r in rows if r['variant']!='reference' and r['form']=='compact']
    passed=equal and len(refs)==60 and all(r['exit_code']==0 for r in refs) and all(r['exit_code']==1 and any(k.endswith('::failure') for k in r['outcomes']) for r in mutants)
    report=dict(status='passed' if passed else 'failed',original_compact_outcomes_identical=equal,paired_implementations=len(pairs),pytest_processes=len(rows),reference_suites=len(refs),reference_test_cases=sum(sum(r['outcomes'].values()) for r in refs),designated_mutants=len(mutants),results=rows)
    (out/'summary.json').write_text(json.dumps(report,indent=2))
    assert passed,'Compact target validation failed; inspect summary'
    data.update(status='passed',executable_validation=str(out.relative_to(ROOT)),executable_validation_sha256=hashlib.sha256((out/'summary.json').read_bytes()).hexdigest())
    (prepared/'report.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
if __name__=='__main__': main()
