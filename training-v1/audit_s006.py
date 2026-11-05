"""Post-run provenance checks; does not change or rescore generated answers."""
import hashlib,json,pathlib,time
EXP=pathlib.Path(__file__).resolve().parents[1]; ROOT=EXP/"training-v1"; STUDY=EXP/"studies/S006-learning-and-transfer"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    frozen=json.loads((STUDY/"freeze-manifest.json").read_text(encoding="utf-8"))
    for name,digest in frozen["files"].items(): assert sha(EXP/name)==digest,name
    report=json.loads((ROOT/"probes/s006-001/report.json").read_text(encoding="utf-8"))
    assert report["status"]=="completed" and len(report["completed"])==24 and not report["unattempted"]
    selection={x["id"]:x for x in json.loads((STUDY/"selection.json").read_text(encoding="utf-8"))["tasks"]}
    reviews=json.loads((STUDY/"source-reviews.json").read_text(encoding="utf-8"))
    for cell in report["completed"]:
        folder=ROOT/"probes/s006-001"/cell["task"]/cell["variant"]
        assert sha(folder/"output.raw.txt")==cell["output_sha256"]
        assert sha(folder/"prompt-token-ids.json")==selection[cell["task"]]["prompt_ids_sha256"]==cell["prompt_ids_sha256"]
        assert sha(folder/"messages.json")==selection[cell["task"]]["messages_sha256"]
        tokens=json.loads((folder/"output-token-ids.json").read_text(encoding="utf-8"))
        assert len(tokens)==cell["generated_tokens"]
        assert bool(tokens and tokens[-1] in (248046,248044))==cell["terminated"]
        candidate=folder/"test_candidate.py"
        if candidate.exists():
            review=reviews[cell["task"]+"/"+cell["variant"]]
            assert review["source_inspected"] and sha(candidate)==review["sha256"]
            works=ROOT/"scoring/s006-001"/cell["task"]/cell["variant"]
            copies=list(works.glob("*/test_candidate.py"))
            if review["approved_for_isolated_execution"]: assert len(copies)==4
            for copy in copies:
                assert sha(copy)==sha(candidate)
                name=copy.parent.name
                evaluator=EXP/"dataset-v1/candidate-006/tasks"/cell["split"]/cell["task"]/"evaluator"
                original=evaluator/"reference/subject.py" if name=="reference" else evaluator/"mutants"/name/"subject.py"
                assert sha(copy.parent/"subject.py")==sha(original)
    assert len(report["reload_checks"])==2 and all(x["max_abs_logit_difference"]==0 for x in report["reload_checks"])
    summary=json.loads((ROOT/"scoring/s006-001/summary.json").read_text(encoding="utf-8"))
    assert {(x["task"],x["variant"]) for x in summary["results"]}=={(x["task"],x["variant"]) for x in report["completed"]}
    result=dict(status="passed",unix_time=time.time(),frozen_files_checked=len(frozen["files"]),generation_cells=24,tasks=8,exact_reload_probes=2,all_prompt_and_raw_output_hashes_match=True,scoring_copies_match_reviewed_sources=True,limits="Checks file/input integrity and report consistency; not independent scientific validation.")
    (STUDY/"integrity-check.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()

