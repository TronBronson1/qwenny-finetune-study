"""Execute original target suites and witnessed mutants; write a new validation report."""
import argparse, concurrent.futures, hashlib, json, os, pathlib, runpy, shutil, subprocess, sys, xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parent
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("dataset")
    p.add_argument("--report",required=True)
    p.add_argument("--python",default=sys.executable)
    p.add_argument("--workers",type=int,default=4)
    p.add_argument("--reuse",help="Reuse complete JUnit executions only when source and target hashes match")
    a=p.parse_args()
    dataset=(ROOT/a.dataset).resolve(); out=(ROOT/a.report).resolve()
    assert dataset.parent==ROOT and out.parent==ROOT and not out.exists()
    manifest=json.loads((dataset/"manifest.json").read_text(encoding="utf-8"))
    hashes=json.loads((dataset/"SHA256.json").read_text(encoding="utf-8"))
    assert all(digest(dataset/name)==expected for name,expected in hashes.items()),"Dataset content changed"
    out.mkdir()
    jobs=[]; explanations=[]
    for record in manifest["tasks"]:
        folder=dataset/"tasks"/record["split"]/record["id"]
        if record["kind"]=="explanation":
            ns=runpy.run_path(str(folder/"evaluator"/"evidence.py"))
            expected=json.loads((folder/"evaluator"/"expected.json").read_text())
            passed=all(ns[k]==v and type(ns[k]) is type(v) for k,v in expected.items())
            explanations.append(dict(id=record["id"],passed=passed,kind="explanation-evidence-only",rubric_scoring="pending-independent-human-review"))
            continue
        jobs.append((record,folder,"reference",folder/"evaluator"/"reference"/"subject.py",None))
        for mutant in json.loads((folder/"evaluator"/"mutants.json").read_text()):
            jobs.append((record,folder,mutant["id"],folder/"evaluator"/"mutants"/mutant["id"]/"subject.py",mutant["witness"]))
        if (folder/"evaluator"/"original-bug"/"subject.py").exists():
            jobs.append((record,folder,"original-bug",folder/"evaluator"/"original-bug"/"subject.py",None))
    version=subprocess.run([a.python,"-c","import sys,pytest; print(sys.version); print('pytest',pytest.__version__)"],capture_output=True,text=True,check=True).stdout
    (out/"runtime.txt").write_text(version,encoding="utf-8")
    def execute(job):
        record,folder,variant,source,witness=job
        work=out/record["id"]/variant
        work.mkdir(parents=True)
        shutil.copyfile(source,work/"subject.py")
        shutil.copyfile(folder/"test_target.py",work/"test_target.py")
        env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8")
        command=[a.python,"-m","pytest","-q","-p","no:cacheprovider","--junitxml=report.xml","test_target.py"]
        reused=False
        if a.reuse:
            prior=ROOT/a.reuse/record["id"]/variant
            if all((prior/name).exists() for name in ("subject.py","test_target.py","report.xml")):
                try:
                    cached=ET.parse(prior/"report.xml").findall(".//testcase")
                    if digest(prior/"subject.py")==digest(source) and digest(prior/"test_target.py")==digest(folder/"test_target.py") and len(cached)>=record["valid_test_cases"]+record["exception_test_cases"]:
                        shutil.copyfile(prior/"report.xml",work/"report.xml")
                        log=(prior/"pytest.log").read_text(encoding="utf-8",errors="replace") if (prior/"pytest.log").exists() else "Recovered complete JUnit report after parent stdout decoding failure; exact source/target hashes match."
                        code=1 if any(t.find("failure") is not None or t.find("error") is not None for t in cached) else 0
                        reused=True
                except (ET.ParseError,OSError): pass
        if not reused:
            try:
                result=subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=20)
                log=result.stdout+result.stderr; code=result.returncode
            except subprocess.TimeoutExpired:
                log="TIMEOUT: no mutant detection credited"; code="timeout"
        (work/"pytest.log").write_text(log,encoding="utf-8")
        tests=[]; meaningful=False
        if (work/"report.xml").exists():
            tests=ET.parse(work/"report.xml").findall(".//testcase")
        if witness:
            name=witness["node"].split("::")[-1]
            for test in tests:
                failure=test.find("failure")
                if test.attrib["name"]==name and failure is not None:
                    text=(failure.text or "")+" "+failure.attrib.get("message","")
                    meaningful=any(token in text for token in ["AssertionError","DID NOT RAISE","assert "])
        if variant=="reference": passed=code==0 and bool(tests)
        elif variant=="original-bug":
            # Seeded regression defect reproduction is separate from mutant scoring.
            passed=code==1 and bool(tests) and any(t.find("failure") is not None for t in tests)
        else: passed=code==1 and meaningful
        return dict(id=record["id"],split=record["split"],variant=variant,passed=passed,exit_code=code,test_cases=len(tests),reused_completed_junit=reused,relevant_witness_verified=meaningful if witness else None,witness=witness)
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(execute,job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            result=future.result(); results.append(result)
            if not result["passed"]: print("FAILED",result["id"],result["variant"],flush=True)
            if len(results)%25==0: print("completed",len(results),"/",len(jobs),flush=True)
    results.sort(key=lambda r:(r["id"],r["variant"]))
    failures=[r for r in results if not r["passed"]]
    summary={"status":"passed" if not failures and all(x["passed"] for x in explanations) else "failed",
        "dataset":str(dataset),"dataset_hash_manifest_sha256":digest(dataset/"SHA256.json"),
        "runtime":version,"reference_suites":sum(r["variant"]=="reference" for r in results),
        "designated_mutants":sum(r["variant"].startswith("M") for r in results),
        "reference_test_cases":sum(r["test_cases"] for r in results if r["variant"]=="reference"),
        "reused_completed_executions":sum(r["reused_completed_junit"] for r in results),
        "seeded_regression_bugs_reproduced":sum(r["variant"]=="original-bug" and r["passed"] for r in results),
        "explanation_evidence":explanations,"failures":failures,"results":results,
        "independence":"Automated same-author checks only; all independent review remains pending."}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("results","runtime","explanation_evidence")},indent=2),flush=True)
    if summary["status"]!="passed": raise SystemExit(1)

if __name__=="__main__": main()
