"""CPU-only selected fixture and interpreter checks, followed by pre-generation freeze."""
import ast,hashlib,json,pathlib,shutil,subprocess,sys,time,os,xml.etree.ElementTree as ET
EXP=pathlib.Path(__file__).resolve().parents[1]
ROOT=EXP/"training-v1"
STUDY=EXP/"studies/S006-learning-and-transfer"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2),encoding="utf-8")
def main():
    assert sys.version_info[:2]==(3,15)
    assert not (STUDY/"freeze-manifest.json").exists()
    for name in ("s006_probe.py","prepare_s006.py","score_s006.py","preflight_s006.py","runtime.py"):
        compile((ROOT/name).read_text(encoding="utf-8"),name,"exec")
    check=subprocess.run([sys.executable,"-m","pytest","--version"],capture_output=True,text=True,check=True)
    assert "pytest 9.2.0" in check.stdout
    selection=json.loads((STUDY/"selection.json").read_text(encoding="utf-8"))["tasks"]
    results=[]; files={}
    def add(p): files[p.relative_to(EXP).as_posix()]=sha(p)
    for name in ("s006_probe.py","prepare_s006.py","score_s006.py","preflight_s006.py","runtime.py"): add(ROOT/name)
    for name in ("selection.json","PROTOCOL_FROZEN.md","REVIEW.md","COVERAGE_RUBRIC.json"): add(STUDY/name)
    for row in selection:
        task=EXP/"dataset-v1/candidate-006/tasks"/row["split"]/row["id"]
        for p in task.rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts: add(p)
        for p in (STUDY/"inputs"/row["id"]).iterdir(): add(p)
        evalu=task/"evaluator"
        variants=[("reference",evalu/"reference/subject.py")]
        variants += [(m["id"],evalu/"mutants"/m["id"]/"subject.py") for m in json.loads((evalu/"mutants.json").read_text(encoding="utf-8"))]
        for variant,source in variants:
            work=STUDY/"preflight"/row["id"]/variant
            work.mkdir(parents=True,exist_ok=False)
            shutil.copyfile(task/"test_target.py",work/"test_candidate.py"); shutil.copyfile(source,work/"subject.py")
            env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8")
            result=subprocess.run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--junitxml=report.xml","test_candidate.py"],cwd=work,env=env,capture_output=True,text=True,encoding="utf-8",timeout=20)
            (work/"pytest.log").write_text(result.stdout+result.stderr,encoding="utf-8")
            tests=ET.parse(work/"report.xml").findall(".//testcase")
            relevant=[t.attrib.get("name") for t in tests if t.find("failure") is not None and any(x in (t.find("failure").text or "")+" "+t.find("failure").attrib.get("message","") for x in ("AssertionError","DID NOT RAISE"))]
            passed=result.returncode==0 and bool(tests) if variant=="reference" else result.returncode==1 and bool(relevant)
            results.append(dict(task=row["id"],variant=variant,exit_code=result.returncode,test_cases=len(tests),relevant_failures=relevant,passed=passed))
            assert passed,(row["id"],variant,result.stdout,result.stderr)
    for epoch in (1,5):
        for name in ("adapter_model.safetensors","adapter_config.json","reload-probe.pt"):
            add(ROOT/"runs/qwenny-001/checkpoints"/f"epoch-{epoch}"/name)
    add(EXP/"lora-feasibility/packages.lock.txt")
    report=dict(status="passed",unix_time=time.time(),python=sys.version,executable=sys.executable,pytest=check.stdout.strip(),results=results,limitations="Selected fixtures checked, not independent semantic validation or an OS security sandbox. Model verification and exact probes occur in generation process.")
    write(STUDY/"preflight.json",report); add(STUDY/"preflight.json")
    freeze=dict(status="frozen-before-generation",unix_time=time.time(),files=files,authorization="User requested moving forward with proposal after reviewing program documentation; local diagnostic only.",review="Same coordinating agent self-review; no separate reviewer claimed.")
    write(STUDY/"freeze-manifest.json",freeze)
    print(json.dumps(dict(preflight=report["status"],checks=len(results),files_frozen=len(files)),indent=2))
if __name__=="__main__": main()

