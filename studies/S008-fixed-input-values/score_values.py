"""Pure JSON scoring; never executes model-generated code."""
import hashlib,json,math,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]; PROBE=EXP/"training-v1/probes/s008-001"
def equal(a,b,typed=False):
    if type(b) is list: return type(a) is list and len(a)==len(b) and all(equal(x,y,typed) for x,y in zip(a,b))
    if type(b) in (int,float):
        return type(a) in (int,float) and (type(a) is int or math.isfinite(a)) and a==b and (not typed or type(a) is type(b))
    return type(a) is type(b) and a==b
def invalid_constant(x): raise ValueError("Nonfinite JSON constant")
def main():
    for name,digest in json.loads((HERE/"freeze-manifest.json").read_text(encoding="utf-8"))["files"].items(): assert hashlib.sha256((EXP/name).read_bytes()).hexdigest()==digest,name
    report=json.loads((PROBE/"report.json").read_text(encoding="utf-8")); assert report["status"] in ("completed","stopped-budget")
    rows=[]
    for cell in report["completed"]:
        answer=(PROBE/cell["task"]/cell["variant"]/"answer.md").read_text(encoding="utf-8").strip()
        expected=json.loads((HERE/"expected"/(cell["task"]+".json")).read_text(encoding="utf-8"))
        text=answer; fence=chr(96)*3
        match=re.fullmatch(fence+r"(?:json)?[ \t]*\n([\s\S]*?)\n"+fence,text)
        fenced=bool(match)
        if match: text=match.group(1).strip()
        error=None; value=None
        try:
            value=json.loads(text,parse_constant=invalid_constant)
            if type(value) is not list or len(value)!=4: raise ValueError("Require outer JSON array of exactly four entries")
            if not cell["terminated"]: raise ValueError("Incomplete first attempt")
        except (ValueError,TypeError) as e: error=str(e)
        correct=[False]*4 if error else [equal(x,y) for x,y in zip(value,expected["values"])]
        typed=[False]*4 if error else [equal(x,y,True) for x,y in zip(value,expected["values"])]
        rows.append(dict(task=cell["task"],split=cell["split"],variant=cell["variant"],case_ids=expected["case_ids"],expected=expected["values"],actual=value,parse_error=error,value_correct=correct,typed_correct=typed,all_four_correct=all(correct),bare_json_compliant=error is None and not fenced,used_json_fence=fenced,terminated=cell["terminated"],tokens=cell["generated_tokens"],seconds=cell["seconds"]))
    groups=[]
    for variant in ("base","original-e1","original-e5"):
        for split in ("training","development"):
            subset=[r for r in rows if r["variant"]==variant and r["split"]==split]
            groups.append(dict(variant=variant,split=split,planned_cases=16,attempted_cases=len(subset)*4,correct_cases=sum(sum(r["value_correct"]) for r in subset),typed_correct_cases=sum(sum(r["typed_correct"]) for r in subset),all_four_tasks=sum(r["all_four_correct"] for r in subset),parseable_tasks=sum(r["parse_error"] is None for r in subset),bare_json_tasks=sum(r["bare_json_compliant"] for r in subset)))
    summary=dict(study="S008",status=report["status"],groups=groups,results=rows,unattempted=report["unattempted"],elapsed_seconds=report["elapsed_seconds"],generation_seconds=sum(c["seconds"] for c in report["completed"]),generated_tokens=sum(c["generated_tokens"] for c in report["completed"]),scope="Supplied-case value accuracy only, not pytest quality or adapter adoption; greedy first attempts on eight visible task families.")
    (HERE/"results.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("results","unattempted")},indent=2))
if __name__=="__main__": main()

