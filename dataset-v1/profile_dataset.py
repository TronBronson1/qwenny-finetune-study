"""CPU-only length profiling. The formatting policy is explicitly provisional."""
import argparse, hashlib, json, pathlib, statistics
from transformers import AutoTokenizer

ROOT=pathlib.Path(__file__).resolve().parent
REV="c202236235762e1c871ad0ccb60c8ee5ba337b9a"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("dataset")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    folder=ROOT/a.dataset; output=ROOT/a.out
    assert not output.exists()
    tokenizer=AutoTokenizer.from_pretrained(ROOT.parent/"lora-feasibility"/"checkpoint"/REV,local_files_only=True)
    records=[json.loads(line) for line in (folder/"training-candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    rows=[]
    for record in records:
        rendered=tokenizer.apply_chat_template(record["messages"],tokenize=False,enable_thinking=False)
        count=len(tokenizer(rendered,add_special_tokens=False)["input_ids"])
        rows.append(dict(id=record["id"],family=record["family"],tokens=count,assistant_text_tokens=len(tokenizer(record["messages"][-1]["content"],add_special_tokens=False)["input_ids"])))
    counts=sorted(r["tokens"] for r in rows)
    summary={"dataset":a.dataset,"base_revision":REV,"training_rows":len(rows),"total_tokens":sum(counts),"minimum":min(counts),"median":statistics.median(counts),"p90_nearest_rank":counts[max(0,__import__("math").ceil(.9*len(counts))-1)],"maximum":max(counts),"rows":rows,"dataset_hash_manifest_sha256":hashlib.sha256((folder/"SHA256.json").read_bytes()).hexdigest(),"formatting_policy":"Thinking disabled for length profiling only; eventual training reasoning/masking policy is not approved.","truncation":"None. Every complete assistant answer was counted.","training_approved":False}
    output.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k!="rows"},indent=2))

if __name__=="__main__": main()
