"""Finalize staging metadata, bind passed code executions, preserve initial hashes."""
import ast,hashlib,json,pathlib,shutil
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]; DATA=EXP/"dataset-v1/candidate-007"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def main():
    certificate=HERE/"calibration-certificate.json"; assert not certificate.exists()
    old=json.loads((DATA/"SHA256.json").read_text(encoding="utf-8")); initial=sha(DATA/"SHA256.json")
    for name,digest in old.items(): assert sha(DATA/name)==digest,name
    summary=json.loads((HERE/"validation-002/summary.json").read_text(encoding="utf-8"))
    assert summary["status"]=="passed" and summary["candidate_manifest_sha256"]==initial
    shutil.copyfile(DATA/"SHA256.json",HERE/"candidate-007-initial-sha256.json")
    build=json.loads((HERE/"build-report.json").read_text(encoding="utf-8")); rows={x["id"]:x for x in build["tasks"]}
    manifest=json.loads((DATA/"manifest.json").read_text(encoding="utf-8")); changes=[]
    for rec in manifest["tasks"]:
        task=DATA/"tasks"/rec["split"]/rec["id"]
        for r in [x for x in summary["results"] if x["task"]==rec["id"]]:
            fixture=task/"evaluator/reference/subject.py" if r["variant"]=="reference" else task/"evaluator/mutants"/r["variant"]/"subject.py"
            executed=HERE/"validation-002"/rec["id"]/r["variant"]
            assert sha(fixture)==sha(executed/"subject.py")
            gold=(task/"test_target.py").read_text(encoding="utf-8")
            copied=(executed/"test_target.py").read_text(encoding="utf-8")
            assert gold==copied
            assert ast.dump(ast.parse(gold))==ast.dump(ast.parse(copied))
        cases=json.loads((task/"evaluator/cases.json").read_text(encoding="utf-8"))
        previous=dict(rec)
        rec.update(oracle_checks=rows[rec["id"]]["oracle_checks"],type_before_value_witnesses=sum(c.get("category")=="type-before-value" for c in cases),pytest_validation="passed S007 validation-002; gold identical after newline normalization; reference/mutants byte-identical",review_status="finite-agent-calibration-passed; revised candidate not independently reviewed",provenance="Contract/oracle-authored derivative of candidate-006 plus documented external adversarial fixture proposals; no failed model output used as a training answer.")
        dump(task/"record.json",rec)
        rubric=json.loads((task/"rubric.json").read_text(encoding="utf-8")); rubric["status"]="finite-agent-category-map-and-execution-calibrated; independent-review-not-claimed"; dump(task/"rubric.json",rubric)
        changes.append(dict(task=rec["id"],metadata_fields_changed=[k for k in rec if previous.get(k)!=rec[k]]))
    manifest["status"]="calibration-passed; no-training-export"
    manifest["validation"]="S007 validation-002; code/fixtures byte-identical at metadata finalization"
    manifest["review_limit"]="Same-agent finite semantic review; external review informed repair, not independent acceptance of revised72-task candidate."
    dump(DATA/"manifest.json",manifest)
    (DATA/"README.md").write_text("# Candidate 007 — calibrated repair, not a training export\n\n60 training and 12 development tasks only. Final/regression tasks are omitted and the original candidate-006 remains intact.\n\nAll 72 revised gold suites passed the correct references (1,475 cases) and rejected all 407 designated mutants through declared witnesses. Five negative controls were correctly rejected. See ../../studies/S007-measurement-repair/calibration-certificate.json and validation-002/summary.json.\n\nThe correct implementations are unchanged. Rubric mappings and instruction wording are explicit; this is finite same-agent calibration, not independent proof of exhaustive correctness. All source examples and fixtures remain inspectable.\n\nNo training approval/export is inherited from the old corpus hash, and no optimizer run used this candidate. One full training chat exceeds the previous 2,048-token fit; see the external token profile before training. Current approved historical exports and CURRENT_CANDIDATE.txt remain unchanged.\n\nbuild-sources preserves the original repair builder and config. finalize_metadata.py is the separate post-validation metadata normalization step. Initial authoring hashes and the code-identical validation binding are preserved outside this snapshot.\n",encoding="utf-8")
    shutil.copyfile(pathlib.Path(__file__),DATA/"build-sources/finalize_metadata.py")
    new={p.relative_to(DATA).as_posix():sha(p) for p in DATA.rglob("*") if p.is_file() and p.name!="SHA256.json"}
    changed=[name for name in old if old[name]!=new[name]]
    assert all(name=="manifest.json" or name=="README.md" or name.endswith(("/record.json","/rubric.json")) for name in changed)
    dump(DATA/"SHA256.json",new)
    dump(certificate,dict(status="passed",initial_candidate_hash=initial,final_candidate_hash=sha(DATA/"SHA256.json"),validation_summary_sha256=sha(HERE/"validation-002/summary.json"),reference_suites=72,reference_cases=1475,designated_mutants=407,negative_controls=5,changed_files=changed,metadata_changes=changes,code_cases_prompts_answers_fixtures_byte_identical_to_validated_snapshot=True,execution_copy_note="Executed gold copies use Windows CRLF; normalized UTF8 text and AST match exactly. Executed reference/mutant copies match bytes.",scope="Calibration repair only; no training export or new independent semantic review. Initial snapshot hashes retained."))
    print(json.dumps(dict(status="passed",changed_metadata_files=len(changed),final_candidate_hash=sha(DATA/"SHA256.json")),indent=2))
if __name__=="__main__": main()

