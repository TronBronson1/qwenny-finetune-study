"""Record actual source/coverage inspection; does not infer approval from tests."""
import argparse,hashlib,json,pathlib,time
EXP=pathlib.Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(); p.add_argument("--task",required=True); p.add_argument("--variant",required=True); p.add_argument("--notes",required=True); p.add_argument("--coverage",choices=("complete","incomplete","not-assessed"),required=True); p.add_argument("--unsafe",action="store_true"); p.add_argument("--claims",default="none observed"); p.add_argument("--prose",choices=("valid","invalid","not-assessed"),default="not-assessed"); a=p.parse_args()
    folder=EXP/"training-v1/probes/s006-001"/a.task/a.variant
    assert (folder/"generation.json").exists()
    candidate=folder/"test_candidate.py"; assert candidate.exists()
    path=EXP/"studies/S006-learning-and-transfer/source-reviews.json"
    records=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    key=a.task+"/"+a.variant; assert key not in records
    records[key]=dict(sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),answer_sha256=hashlib.sha256((folder/"answer.md").read_bytes()).hexdigest(),approved_for_isolated_execution=not a.unsafe,source_inspected=True,reviewer="coordinating agent; manual source inspection, no independent review claimed",unix_time=time.time(),coverage_status=a.coverage,notes=a.notes,execution_claim_review=a.claims,reason=a.notes if a.unsafe else None)
    records[key]["prose_status"]=a.prose
    path.write_text(json.dumps(records,indent=2),encoding="utf-8")
    print(key)
if __name__=="__main__": main()

