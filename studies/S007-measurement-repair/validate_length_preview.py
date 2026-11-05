"""Validate only the changed TR058 presentation against all seven existing fixtures."""
import ast,hashlib,json,os,pathlib,shutil,subprocess,sys,xml.etree.ElementTree as ET
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]; PREVIEW=HERE/"length-preview-002"; TASK=EXP/"dataset-v1/candidate-007/tasks/training/TR058"; OUT=PREVIEW/"validation"
def normalize(text):
    tree=ast.parse(text)
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="pytest" and n.func.attr=="param": n.keywords=[k for k in n.keywords if k.arg!="id"]
    return ast.dump(tree,include_attributes=False)
def vector(path):
    return [(t.attrib["name"].split("[")[0],t.find("failure") is not None,t.find("error") is not None,t.find("skipped") is not None) for t in ET.parse(path).findall(".//testcase")]
def main():
    assert not OUT.exists(); OUT.mkdir()
    gold=(TASK/"test_target.py").read_text(encoding="utf-8"); compact=(PREVIEW/"test_target.py").read_text(encoding="utf-8")
    assert normalize(gold)==normalize(compact)
    profile=json.loads((PREVIEW/"profile.json").read_text(encoding="utf-8")); assert profile["within_previous2048"]
    variants=[("reference",TASK/"evaluator/reference/subject.py")]+[(m["id"],TASK/"evaluator/mutants"/m["id"]/"subject.py") for m in json.loads((TASK/"evaluator/mutants.json").read_text(encoding="utf-8"))]
    results=[]; env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8")
    for name,source in variants:
        work=OUT/name; work.mkdir()
        shutil.copyfile(source,work/"subject.py"); (work/"test_target.py").write_text(compact,encoding="utf-8",newline="\n")
        run=subprocess.run([sys.executable,"-m","pytest","-q","-p","no:cacheprovider","--junitxml=report.xml","test_target.py"],cwd=work,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=20)
        (work/"pytest.log").write_text(run.stdout+run.stderr,encoding="utf-8")
        expected=0 if name=="reference" else 1
        assert run.returncode==expected,(name,run.returncode)
        current=vector(work/"report.xml"); previous=vector(HERE/"validation-002/TR058"/name/"report.xml")
        assert current==previous,(name,"case result vector changed")
        results.append(dict(variant=name,exit_code=run.returncode,cases=len(current),all_per_case_results_identical=True))
    report=dict(status="passed",scope="TR058 presentation preview only; no export/training or change to candidate-007.",ast_equal_ignoring_display_ids=True,profile=profile,results=results)
    (PREVIEW/"validation.json").write_text(json.dumps(report,indent=2),encoding="utf-8"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()

