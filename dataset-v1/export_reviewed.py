"""Export training messages only after exact-content validation and independent review."""
import argparse, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",required=True)
    p.add_argument("--validation",required=True)
    review=p.add_mutually_exclusive_group(required=True)
    review.add_argument("--approvals")
    review.add_argument("--corpus-approval",help="Explicit user corpus-review and training authorization, bound to the exact candidate")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    dataset=(ROOT/a.dataset).resolve(); out=(ROOT/a.out).resolve()
    assert dataset.parent==ROOT and out.parent==ROOT and not out.exists()
    validation=json.loads((ROOT/a.validation/"summary.json").read_text(encoding="utf-8"))
    hashes=json.loads((dataset/"SHA256.json").read_text(encoding="utf-8"))
    assert validation["status"]=="passed","Automated validation must pass"
    assert validation["dataset_hash_manifest_sha256"]==sha(dataset/"SHA256.json"),"Validation belongs to different data"
    assert all(sha(dataset/name)==expected for name,expected in hashes.items()),"Dataset changed since validation"
    manifest=json.loads((dataset/"manifest.json").read_text(encoding="utf-8"))
    training=[r for r in manifest["tasks"] if r["split"]=="training"]
    if a.corpus_approval:
        approval=json.loads(pathlib.Path(a.corpus_approval).read_text(encoding="utf-8"))
        assert approval.get("reviewed") is True and approval.get("training_authorized") is True and approval.get("reviewer"),"Explicit reviewed-corpus training authorization required"
        assert approval.get("dataset_hash_manifest_sha256")==sha(dataset/"SHA256.json"),"Corpus approval hash mismatch"
        assert approval.get("dataset")==dataset.name and approval.get("user_statements"),"Corpus approval scope missing"
        basis={"kind":"explicit-user-corpus-review-and-training-authorization","record":str(pathlib.Path(a.corpus_approval).resolve()),"per_record_review_log_asserted":False}
    else:
        approvals=json.loads(pathlib.Path(a.approvals).read_text(encoding="utf-8"))
        assert approvals.get("family_audit_complete") is True and approvals.get("family_audit_reviewer"),"Independent family/split audit required"
        approved={r["id"]:r for r in approvals["tasks"]}
        for record in training:
            review=approved[record["id"]]
            assert review.get("approved") is True and review.get("reviewer") and review.get("review_notes"),f'Independent review pending: {record["id"]}'
            for key in ("source_sha256","spec_sha256","target_sha256","answer_sha256"):
                assert review.get(key)==record[key],f'Reviewed hash mismatch: {record["id"]} {key}'
        basis={"kind":"per-record-independent-review","record":str(pathlib.Path(a.approvals).resolve())}
    rows=[json.loads(line) for line in (dataset/"training-candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows)==len(training)==60
    assert {r["id"] for r in rows}=={r["id"] for r in training}
    # Only model messages are exported: no references, oracle code, mutants or held-out answers.
    text="".join(json.dumps({"messages":r["messages"]},ensure_ascii=False)+"\n" for r in rows)
    out.mkdir()
    (out/"train.jsonl").write_text(text,encoding="utf-8")
    (out/"provenance.json").write_text(json.dumps({"dataset":a.dataset,"training_ids":[r["id"] for r in rows],"validation_hash_manifest":validation["dataset_hash_manifest_sha256"],"train_sha256":sha(out/"train.jsonl"),"approval_basis":basis,"reasoning_masking_policy":"Must be separately pinned and checked in training configuration; this export contains direct assistant targets."},indent=2),encoding="utf-8")
    print("Exported",len(rows),"training records with approval basis",basis["kind"],"to",out)

if __name__=="__main__": main()
