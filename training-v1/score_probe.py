"""Score reference/mutant execution only after hash-bound agent code inspection."""
import argparse,ast,concurrent.futures,hashlib,json,os,pathlib,re,shutil,subprocess,xml.etree.ElementTree as ET
from runtime import ROOT,EXP

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect_ast(text,function):
    tree=ast.parse(text)
    allowed={"pytest","subject","copy","math","itertools","functools","collections","re","string","typing"}
    for node in ast.walk(tree):
        if isinstance(node,ast.Import) and any(n.name.split(".")[0] not in allowed for n in node.names): raise ValueError("Unapproved import")
        if isinstance(node,ast.ImportFrom):
            module=(node.module or "").split(".")[0]
            safe_builtin=module=="builtins" and all(n.name in {"int","str","float","bool","tuple","list","dict","set","bytes","object","type"} for n in node.names)
            if module not in allowed and not safe_builtin: raise ValueError("Unapproved from-import")
        if isinstance(node,ast.FunctionDef) and node.name==function: raise ValueError("Target function replaced")
        if isinstance(node,ast.Attribute) and node.attr.startswith("__"): raise ValueError("Dunder introspection")
        if isinstance(node,ast.Name) and node.id in {"eval","exec","compile","open","__import__","globals","locals","getattr","setattr","delattr","vars"}: raise ValueError("Dynamic inspection/execution")
        if isinstance(node,(ast.While,ast.AsyncFunctionDef,ast.Await)): raise ValueError("Unbounded or asynchronous test code")
    return True

def main():
    p=argparse.ArgumentParser(); p.add_argument("--probe",required=True); p.add_argument("--reviews",required=True); p.add_argument("--out",required=True)
    p.add_argument("--python",required=True); a=p.parse_args()
    probe=ROOT/a.probe; out=ROOT/a.out; assert not out.exists()
    report=json.loads((probe/"report.json").read_text()); assert report["status"]=="completed"
    reviews=json.loads(pathlib.Path(a.reviews).read_text(encoding="utf-8"))
    out.mkdir(parents=True)
    corpus=EXP/"dataset-v1"/"candidate-006"; summaries=[]; jobs=[]
    for generated in report["completed"]:
        task,label=generated["task"],generated["variant"]
        folder=probe/task/label; candidate=folder/"test_candidate.py"
        item=dict(task=task,variant=label,truncated=generated["truncated"],format_valid=generated["python_blocks"]==1,strict_acceptance="pending category/prose review; this is not final-test scoring")
        summaries.append(item)
        if not candidate.exists(): item.update(execution="no-single-code-block",provisional_executable_pass=False); continue
        review=reviews.get(task+"/"+label,{})
        assert review.get("approved_for_isolated_execution") is True and review.get("sha256")==sha(candidate),"Candidate code inspection required"
        record=json.loads((corpus/"tasks"/"development"/task/"record.json").read_text())
        try:
            inspect_ast(candidate.read_text(encoding="utf-8"),record["function"])
            item["syntax"]="parsed"
        except SyntaxError:
            # Python cannot execute an unparseable module; retain its collection failure.
            item["syntax"]="invalid; collection failure expected"
        fixtures=corpus/"tasks"/"development"/task/"evaluator"
        variants=[("reference",fixtures/"reference"/"subject.py")]
        variants += [(m["id"],fixtures/"mutants"/m["id"]/"subject.py") for m in json.loads((fixtures/"mutants.json").read_text())]
        for name,source in variants: jobs.append((item,candidate,name,source))
    def execute(job):
        item,candidate,name,source=job
        work=out/item["task"]/item["variant"]/name; work.mkdir(parents=True)
        shutil.copyfile(candidate,work/"test_candidate.py"); shutil.copyfile(source,work/"subject.py")
        env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8")
        try:
            r=subprocess.run([a.python,"-m","pytest","-q","-p","no:cacheprovider","--junitxml=report.xml","test_candidate.py"],cwd=work,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=20)
            code=r.returncode; text=r.stdout+r.stderr
        except subprocess.TimeoutExpired: code="timeout"; text="TIMEOUT: not a valid mutant detection"
        (work/"pytest.log").write_text(text,encoding="utf-8")
        tests=ET.parse(work/"report.xml").findall(".//testcase") if (work/"report.xml").exists() else []
        relevant=[]
        for test in tests:
            failure=test.find("failure")
            if failure is not None and any(s in (failure.text or "")+" "+failure.attrib.get("message","") for s in ("AssertionError","DID NOT RAISE")):
                relevant.append(test.attrib.get("name"))
        return (item["task"],item["variant"],name,dict(exit_code=code,test_cases=len(tests),relevant_failures=relevant))
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for task,label,name,result in pool.map(execute,jobs): results.setdefault((task,label),{})[name]=result
    for item in summaries:
        variants=results.get((item["task"],item["variant"]))
        if not variants: continue
        reference=variants["reference"]["exit_code"]==0 and variants["reference"]["test_cases"]>0
        kills=sum(v["exit_code"]==1 and bool(v["relevant_failures"]) for name,v in variants.items() if name!="reference")
        answer=(probe/item["task"]/item["variant"]/"answer.md").read_text(encoding="utf-8")
        flags=re.findall(r"\b(?:I|we)\s+(?:ran|executed|tested)\b|\ball tests (?:pass|passed)\b",answer,re.I)
        item.update(execution="completed",reference_valid=reference,eligible_mutant_kills=kills if reference else None,designated_mutants=3,variants=variants,execution_claim_flags=flags,provisional_executable_pass=reference and kills==3 and item["format_valid"] and not item["truncated"])
    final={"scope":"Two visible development families, seed 42, bounded direct-answer pilot; no strict acceptance claim without category/prose review.","results":summaries}
    (out/"summary.json").write_text(json.dumps(final,indent=2),encoding="utf-8")
    print(json.dumps([{k:v for k,v in row.items() if k!="variants"} for row in summaries],indent=2))

if __name__=="__main__": main()
