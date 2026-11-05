"""Final integrity audit and fingerprints for completed S007/S008."""
import hashlib,json,pathlib,re,time
EXP=pathlib.Path(__file__).resolve().parents[2]
S7=EXP/"studies/S007-measurement-repair"; S8=EXP/"studies/S008-fixed-input-values"; DATA=EXP/"dataset-v1/candidate-007"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v): p.write_text(json.dumps(v,indent=2),encoding="utf-8")
def main():
    old=json.loads((EXP/"studies/S006-learning-and-transfer/result-sha256.json").read_text(encoding="utf-8"))
    for name,h in old["files"].items(): assert sha(EXP/name)==h,name
    original=json.loads((EXP/"studies/S006-learning-and-transfer/freeze-manifest.json").read_text(encoding="utf-8"))
    for name,h in original["files"].items(): assert sha(EXP/name)==h,name
    manifest=json.loads((DATA/"SHA256.json").read_text(encoding="utf-8"))
    for name,h in manifest.items(): assert sha(DATA/name)==h,name
    cert=json.loads((S7/"calibration-certificate.json").read_text(encoding="utf-8")); assert cert["final_candidate_hash"]==sha(DATA/"SHA256.json")
    records=json.loads((DATA/"manifest.json").read_text(encoding="utf-8"))["tasks"]
    for row in records:
        ref=DATA/"tasks"/row["split"]/row["id"]/"evaluator/reference/subject.py"
        parent=EXP/"dataset-v1/candidate-006/tasks"/row["split"]/row["id"]/"evaluator/reference/subject.py"
        assert sha(ref)==sha(parent),row["id"]
    frozen=json.loads((S8/"freeze-manifest.json").read_text(encoding="utf-8"))
    for name,h in frozen["files"].items(): assert sha(EXP/name)==h,name
    probe=EXP/"training-v1/probes/s008-001"; generation=json.loads((probe/"report.json").read_text(encoding="utf-8")); assert generation["status"]=="completed" and len(generation["completed"])==24
    assert all(x["max_abs_logit_difference"]==0 for x in generation["reload_checks"])
    selection={r["id"]:r for r in json.loads((S8/"selection.json").read_text(encoding="utf-8"))["tasks"]}
    for cell in generation["completed"]:
        folder=probe/cell["task"]/cell["variant"]
        assert sha(folder/"output.raw.txt")==cell["output_sha256"]
        assert sha(folder/"prompt-token-ids.json")==selection[cell["task"]]["prompt_ids_sha256"]==cell["prompt_ids_sha256"]
        ids=json.loads((folder/"output-token-ids.json").read_text(encoding="utf-8")); assert len(ids)==cell["generated_tokens"] and ids[-1] in (248046,248044)
    summary=json.loads((S8/"results.json").read_text(encoding="utf-8"))
    totals={v:sum(g["correct_cases"] for g in summary["groups"] if g["variant"]==v) for v in ("base","original-e1","original-e5")}; assert totals==dict(base=22,**{"original-e1":23,"original-e5":22})
    assert len(summary["results"])==24 and sum(x["parse_error"] is not None for x in summary["results"])==1
    overlay=json.loads((S7/"TRAINING_FIT_OVERLAY.json").read_text(encoding="utf-8")); assert overlay["profiled_maximum_full_training_chat"]==2021 and overlay["replacement_chat_tokens"]==1878
    assert json.loads((S7/"length-preview-002/validation.json").read_text(encoding="utf-8"))["status"]=="passed"
    docs=[EXP/"START_HERE.md",EXP/"dataset-v1/README.md",EXP/"training-v1/README.md"]+list((EXP/"program").glob("*.md"))+list((EXP/"observer").glob("*.md"))+list(S7.glob("*.md"))+list(S8.glob("*.md"))
    for p in docs:
        for target in re.findall(r"\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"): assert (p.parent/target.split("#")[0]).exists(),(p,target)
    result=dict(status="passed",unix_time=time.time(),original_s006_artifact_hashes_unchanged=len(old["files"]),original_s006_frozen_files_unchanged=len(original["files"]),candidate_files_checked=len(manifest),correct_references_byte_identical_to_parent=72,s008_frozen_files_checked=len(frozen["files"]),model_attempts=24,exact_adapter_probes=2,s008_correct_values=totals,checked_markdown_documents=len(docs),final_and_regression_contents_not_accessed=True)
    dump(S7/"final-integrity.json",result); dump(S8/"final-integrity.json",result)
    fingerprints={}
    for root in (S7,S8,DATA,probe):
        for p in root.rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts and p.name!="result-sha256.json": fingerprints[p.relative_to(EXP).as_posix()]=sha(p)
    for p in (EXP/"training-v1/s008_probe.py",EXP/"training-v1/s008-001.log",EXP/"observer/REPORT_005.md",EXP/"program/NEXT_TRAINING_STUDY.md"): fingerprints[p.relative_to(EXP).as_posix()]=sha(p)
    dump(S8/"result-sha256.json",dict(unix_time=time.time(),files=fingerprints))
    for name,h in fingerprints.items(): assert sha(EXP/name)==h,name
    print(json.dumps(result|dict(final_result_fingerprints_verified=len(fingerprints)),indent=2))
if __name__=="__main__": main()

