"""Combine unchanged executable scoring with explicit frozen-rubric source review."""
import csv,hashlib,json,pathlib,time,collections
EXP=pathlib.Path(__file__).resolve().parents[1]; ROOT=EXP/"training-v1"; STUDY=EXP/"studies/S006-learning-and-transfer"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8")
def main():
    probe=ROOT/"probes/s006-001"; scoring=ROOT/"scoring/s006-001"
    generation=json.loads((probe/"report.json").read_text(encoding="utf-8"))
    assert generation["status"] in ("completed","stopped-budget")
    scores=json.loads((scoring/"summary.json").read_text(encoding="utf-8"))["results"]
    reviews=json.loads((STUDY/"source-reviews.json").read_text(encoding="utf-8"))
    cells={(x["task"],x["variant"]):x for x in generation["completed"]}
    assert len(scores)==len(cells)
    for row in scores:
        cell=cells[(row["task"],row["variant"])]; folder=probe/row["task"]/row["variant"]
        review=reviews.get(row["task"]+"/"+row["variant"])
        if (folder/"test_candidate.py").exists():
            assert review and review["source_inspected"] and review["sha256"]==sha(folder/"test_candidate.py")
            assert review["answer_sha256"]==sha(folder/"answer.md")
        row.update(generated_tokens=cell["generated_tokens"],seconds=cell["seconds"],stop_reason=cell["stop_reason"],review=review)
        row["strict_accepted"]=bool(row.get("provisional_executable_pass") and review and review["coverage_status"]=="complete" and review.get("prose_status")=="valid")
        reasons=[]
        if row["truncated"]: reasons.append("incomplete generation")
        if not row["format_valid"]: reasons.append("missing single complete code block")
        if not row.get("reference_valid",False): reasons.append("reference not valid or not executable")
        if row.get("reference_valid") and row.get("eligible_mutant_kills")!=row.get("designated_mutants"): reasons.append("required mutant detection incomplete")
        if review and review["coverage_status"]!="complete": reasons.append("frozen contract coverage incomplete/not fully assessed")
        if review and review.get("prose_status")!="valid": reasons.append("mapping/claims review not valid or not fully assessed")
        row["rejection_reasons"]=reasons if not row["strict_accepted"] else []
    groups=[]
    for split in ("training","development"):
        for variant in ("base","original-e1","original-e5"):
            rows=[x for x in scores if x["split"]==split and x["variant"]==variant]
            groups.append(dict(split=split,variant=variant,planned=4,attempted=len(rows),completed=sum(not x["truncated"] for x in rows),reference_valid=sum(bool(x.get("reference_valid")) for x in rows),reference_and_mutants=sum(bool(x.get("reference_valid") and x.get("eligible_mutant_kills")==3) for x in rows),strict_accepted=sum(x["strict_accepted"] for x in rows)))
    gpu=[]
    with (probe/"gpu-memory.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try: gpu.append(float(row["free_MiB"]))
            except (ValueError,TypeError): pass
    process=[]
    path=probe/"windows-process-memory.csv"
    if path.exists():
        with path.open(encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                try: process.append(dict(dedicated=int(row["dedicated_bytes"]),shared=int(row["shared_bytes"])))
                except (ValueError,TypeError,KeyError): pass
    result=dict(study="S006",run="s006-001",status=generation["status"],scope="Exploratory purposive four-family familiar-training and four-family development diagnostic, one seed. No candidate selection, causal mechanism, or general aptitude claim.",groups=groups,results=scores,unattempted=generation["unattempted"],runtime=dict(generation_and_preflight_seconds=generation.get("elapsed_seconds"),generation_seconds=sum(x["seconds"] for x in generation["completed"]),total_generated_tokens=sum(x["generated_tokens"] for x in generation["completed"]),peak_torch_allocated=max(x["memory"]["peak_allocated"] for x in generation["completed"]),peak_torch_reserved=max(x["memory"]["peak_reserved"] for x in generation["completed"]),gpu_sample_min_free_MiB=min(gpu) if gpu else None,process_samples=len(process),process_peak_shared_bytes=max(x["shared"] for x in process) if process else None),review_limit="Source/rubric review by same coordinating agent; not independent scientific validation.",frozen_protocol_sha256=sha(STUDY/"PROTOCOL_FROZEN.md"),freeze_manifest_sha256=sha(STUDY/"freeze-manifest.json"),source_reviews_sha256=sha(STUDY/"source-reviews.json"))
    write(STUDY/"results.json",result)
    text=["# S006 results — learning, transfer, and completion","", "November 4, 2026 (America/New_York). Exploratory local RTX3080 diagnostic; see [frozen protocol](PROTOCOL_FROZEN.md).", "", "## Summary", "", "| Split | Model | Attempted/planned | Complete | Reference-valid | Reference + all mutants | Strict accepted |","|---|---|---:|---:|---:|---:|---:|"]
    for g in groups: text.append("| {split} | {variant} | {attempted}/{planned} | {completed} | {reference_valid} | {reference_and_mutants} | {strict_accepted} |".format(**g))
    text+=["","Counts are out of four tasks per split/arm. Training tasks are familiar, not transfer evidence. All development targets previously contributed teacher-forced loss. Exact sampled tasks are in selection.json; no random-sample or population estimate is claimed.","","## Every first attempt","","| Task | Model | Tokens | Stop | Reference-valid | Eligible mutant kills | Strict |","|---|---|---:|---|---|---|---|"]
    for x in scores:
        text.append(f'| {x["task"]} | {x["variant"]} | {x["generated_tokens"]} | {x["stop_reason"]} | {bool(x.get("reference_valid"))} | {x.get("eligible_mutant_kills")} | {x["strict_accepted"]} |')
    text+=["","## Source and rubric findings",""]
    for x in scores:
        review=x.get("review")
        text.append(f'- **{x["task"]}/{x["variant"]}:** '+(review["notes"] if review else "No complete single candidate file; no repaired source executed."))
    t=result["runtime"]
    text+=["","## Runtime and limitations","",f'Model verification/loading/generation elapsed: {t["generation_and_preflight_seconds"]:.1f} seconds. Generation cells: {t["generation_seconds"]:.1f} seconds; {t["total_generated_tokens"]} generated tokens. Torch peak allocated/reserved: {t["peak_torch_allocated"]/1024**3:.2f}/{t["peak_torch_reserved"]/1024**3:.2f} GiB. GPU sampled minimum free: {t["gpu_sample_min_free_MiB"]} MiB. Windows per-process memory samples: {t["process_samples"]}; missing process samples cannot establish shared-memory spill. Scoring/pre-generation CPU fixture checks and report preparation are outside generation timing.', "", "One seed and four purposively selected families per split cannot establish general aptitude or isolate a failure mechanism. Training and development task sets differ in content and difficulty. No final/regression tasks, new training, retries, repairs, cloud, conversion or LM Studio changes. Same-agent source review and fixture checks are not independent scientific validation.","","## Evidence","","- [Machine results](results.json) and [source reviews](source-reviews.json).","- [Generation records](../../training-v1/probes/s006-001/report.json).","- [Unchanged execution results](../../training-v1/scoring/s006-001/summary.json).","- [Preflight](preflight.json), [frozen hashes](freeze-manifest.json), [coverage rubric](COVERAGE_RUBRIC.json).","- Interpretation and next decision are recorded separately in INTERPRETATION.md after reviewing these results.",""]
    (STUDY/"RESULTS.md").write_text("\n".join(text),encoding="utf-8")
    fingerprints={}
    for root in (probe,scoring,STUDY):
        for p in root.rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts and p.name!="result-sha256.json": fingerprints[p.relative_to(EXP).as_posix()]=sha(p)
    for name in ("finalize_s006.py","record_s006_review.py","audit_s006.py","s006-001.log","s006-001-scoring.log"):
        p=ROOT/name
        if p.exists(): fingerprints[p.relative_to(EXP).as_posix()]=sha(p)
    write(STUDY/"result-sha256.json",dict(unix_time=time.time(),files=fingerprints))
    print(json.dumps(dict(groups=groups,runtime=t),indent=2))
if __name__=="__main__": main()

