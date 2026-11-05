"""Execute revised gold calibration; no models or reserved task content."""
import ast,concurrent.futures,hashlib,json,os,pathlib,shutil,subprocess,sys,time,xml.etree.ElementTree as ET
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]; DATA=EXP/"dataset-v1/candidate-007"; OUT=HERE/"validation-001"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v): p.write_text(json.dumps(v,indent=2),encoding="utf-8")
def meaningful_source(text,function):
    try: tree=ast.parse(text)
    except SyntaxError: return False
    tests=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith("test_")]
    return bool(tests) and any(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==function for n in ast.walk(t)) and any(isinstance(n,ast.Assert) or isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="raises" for n in ast.walk(t)) for t in tests)
def classify(code,tests,witness=None,meaningful=True):
    if witness is None: return code==0 and bool(tests) and meaningful and not any(t.find("skipped") is not None or t.find("failure") is not None or t.find("error") is not None for t in tests)
    if code!=1: return False
    name=witness["node"].split("::")[-1]
    for t in tests:
        failure=t.find("failure")
        if t.attrib.get("name")!=name or failure is None: continue
        message=failure.attrib.get("message",""); text=(failure.text or "")+" "+message
        if witness["kind"]=="result-or-post-state-assertion": return "AssertionError" in text or "assert " in text and message.startswith("assert")
        if witness["kind"]=="required-exception-not-raised": return "DID NOT RAISE" in text
        if witness["kind"]=="required-exception-wrong-class":
            actual=witness["actual_exception"]
            return actual in ("TypeError","ValueError","IndexError") and message.startswith(actual+":")
    return False
def execute(job):
    ident,variant,source,target,witness,function=job
    work=OUT/ident/variant; work.mkdir(parents=True)
    shutil.copyfile(source,work/"subject.py")
    (work/"test_target.py").write_text(target,encoding="utf-8")
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8")
    begin=time.monotonic()
    try:
        run=subprocess.run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--junitxml=report.xml","test_target.py"],cwd=work,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=20)
        code=run.returncode; text=run.stdout+run.stderr
    except subprocess.TimeoutExpired: code="timeout"; text="Timeout is not defect detection"
    (work/"pytest.log").write_text(text,encoding="utf-8")
    tests=ET.parse(work/"report.xml").findall(".//testcase") if (work/"report.xml").exists() else []
    meaningful=meaningful_source(target,function)
    return dict(task=ident,variant=variant,exit_code=code,test_cases=len(tests),skipped=sum(t.find("skipped") is not None for t in tests),meaningful_test_present=meaningful,passed=classify(code,tests,witness,meaningful),seconds=time.monotonic()-begin,witness=witness)
def main():
    assert sys.version_info[:2]==(3,15) and not OUT.exists()
    manifest=json.loads((DATA/"manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["tasks"])==72 and all(r["split"] in ("training","development") for r in manifest["tasks"])
    hashes=json.loads((DATA/"SHA256.json").read_text(encoding="utf-8"))
    for name,digest in hashes.items(): assert sha(DATA/name)==digest,name
    OUT.mkdir()
    version=subprocess.run([sys.executable,"-c","import sys,pytest; print(sys.version); print(pytest.__version__)"],capture_output=True,text=True,check=True).stdout
    (OUT/"runtime.txt").write_text(version,encoding="utf-8")
    shutil.copyfile(pathlib.Path(__file__),OUT/"validate_repair.py")
    jobs=[]
    for rec in manifest["tasks"]:
        task=DATA/"tasks"/rec["split"]/rec["id"]; target=(task/"test_target.py").read_text(encoding="utf-8")
        assert meaningful_source(target,rec["function"]),rec["id"]
        jobs.append((rec["id"],"reference",task/"evaluator/reference/subject.py",target,None,rec["function"]))
        for m in json.loads((task/"evaluator/mutants.json").read_text(encoding="utf-8")):
            jobs.append((rec["id"],m["id"],task/"evaluator/mutants"/m["id"]/"subject.py",target,m["witness"],rec["function"]))
    begin=time.monotonic(); results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(execute,jobs):
            results.append(result)
            if not result["passed"]: print("FAILED",result["task"],result["variant"],flush=True)
            if len(results)%25==0:
                dump(OUT/"progress.json",dict(completed=len(results),total=len(jobs)))
                print("completed",len(results),"/",len(jobs),flush=True)
    # Actual execution negative controls: collected tests alone are not enough.
    ref=DATA/"tasks/training/TR049/evaluator/reference/subject.py"
    examples={
        "empty":"",
        "pass-only":"def test_noop(): pass\n",
        "assert-true-only":"from subject import row_major_offset\ndef test_noop(): assert True\n",
        "skip-only":"import pytest\nfrom subject import row_major_offset\n@pytest.mark.skip(reason='negative control')\ndef test_skipped(): assert row_major_offset(0,0,1,1)==0\n"}
    controls=[]
    for label,text in examples.items():
        result=execute(("NEGATIVE",label,ref,text,None,"row_major_offset")); assert not result["passed"],label; controls.append(result)
    crashing=OUT/"crashing_subject.py"; crashing.write_text("def row_major_offset(*args): raise RuntimeError('unrelated crash')\n",encoding="utf-8")
    target='from subject import row_major_offset\ndef test_value(): assert row_major_offset(0,0,1,1)==0\n'
    witness=dict(node="test_target.py::test_value",kind="result-or-post-state-assertion")
    result=execute(("NEGATIVE","unrelated-crash",crashing,target,witness,"row_major_offset")); assert not result["passed"]; controls.append(result)
    failures=[r for r in results if not r["passed"]]
    summary=dict(status="passed" if not failures else "failed",candidate="candidate-007",candidate_manifest_sha256=sha(DATA/"SHA256.json"),runtime=version,elapsed_seconds=time.monotonic()-begin,reference_suites=sum(x["variant"]=="reference" for x in results),reference_cases=sum(x["test_cases"] for x in results if x["variant"]=="reference"),designated_mutants=sum(x["variant"]!="reference" for x in results),wrong_exception_witnesses=sum(x.get("witness") is not None and x["witness"]["kind"]=="required-exception-wrong-class" for x in results),failures=failures,negative_controls=controls,results=results,review_limit="Finite gold calibration plus agent semantic review, not independent72-task scientific validation or exhaustive coverage. No model generation or training.")
    dump(OUT/"summary.json",summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ("results","runtime","negative_controls")},indent=2),flush=True)
    if failures: raise SystemExit(1)
if __name__=="__main__": main()

