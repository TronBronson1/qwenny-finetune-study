"""Exact answer-only tokenization; never truncate or supervise prompt/thinking markup."""
import argparse, hashlib, json, pathlib
from transformers import AutoTokenizer

ROOT=pathlib.Path(__file__).resolve().parent
EXP=ROOT.parent
REV="c202236235762e1c871ad0ccb60c8ee5ba337b9a"
CHECKPOINT=EXP/"lora-feasibility"/"checkpoint"/REV

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def encode_answer(tokenizer,messages,ident,max_length):
    assert messages[-1]["role"]=="assistant"
    full=tokenizer.apply_chat_template(messages,tokenize=False,enable_thinking=True,add_generation_prompt=False)
    prefix=tokenizer.apply_chat_template(messages[:-1],tokenize=False,enable_thinking=False,add_generation_prompt=True)
    assert full.startswith(prefix) and prefix.endswith("<think>\n\n</think>\n\n"),ident
    assert full.endswith("<|im_end|>\n")
    start,end=len(prefix),len(full)-1
    encoded=tokenizer(full,add_special_tokens=False,return_offsets_mapping=True)
    ids=encoded["input_ids"]; offsets=encoded["offset_mapping"]
    assert len(ids)<=max_length,(ident,len(ids),max_length)
    assert all(not (a<start<b or a<end<b) for a,b in offsets),f"Token crosses supervision boundary: {ident}"
    labels=[token if a>=start and b<=end and b>a else -100 for token,(a,b) in zip(ids,offsets)]
    supervised=[v for v in labels if v!=-100]
    assert len(supervised)>1 and supervised[-1]==tokenizer.convert_tokens_to_ids("<|im_end|>")
    decoded=tokenizer.decode(supervised,skip_special_tokens=False,clean_up_tokenization_spaces=False)
    assert decoded==messages[-1]["content"].strip()+"<|im_end|>",ident
    first=next(i for i,v in enumerate(labels) if v!=-100)
    assert all(v==-100 for v in labels[:first]) and labels[-1]==-100
    return dict(id=ident,input_ids=ids,labels=labels,input_tokens=len(ids),target_tokens=len(supervised),first_target_token=first,
                target_text_sha256=hashlib.sha256(decoded.encode()).hexdigest())

def main():
    p=argparse.ArgumentParser(); p.add_argument("--out",required=True); a=p.parse_args()
    out=ROOT/a.out
    assert out.parent==ROOT and not out.exists()
    export=EXP/"dataset-v1"/"training-approved-001"
    provenance=json.loads((export/"provenance.json").read_text())
    assert sha(export/"train.jsonl")==provenance["train_sha256"]
    tokenizer=AutoTokenizer.from_pretrained(CHECKPOINT,local_files_only=True)
    rows=[json.loads(line) for line in (export/"train.jsonl").read_text(encoding="utf-8").splitlines()]
    train=[encode_answer(tokenizer,r["messages"],ident,2048) for ident,r in zip(provenance["training_ids"],rows)]
    assert len(train)==60
    corpus=EXP/"dataset-v1"/"candidate-006"
    requests=[json.loads(line) for line in (corpus/"model-packets"/"development-requests.jsonl").read_text(encoding="utf-8").splitlines()]
    demonstrations=[]
    for ident in ("D01","D02"):
        folder=EXP/"prompt-comparison"/"demonstrations"/ident
        demonstrations += [dict(role="user",content=(folder/"SPEC.md").read_text(encoding="utf-8").strip()),dict(role="assistant",content=(folder/"ANSWER.md").read_text(encoding="utf-8").strip())]
    development=[]
    for request in requests:
        answer=(corpus/"tasks"/"development"/request["id"]/"TARGET.md").read_text(encoding="utf-8")
        for arm in ("A","B"):
            messages=request["messages"]
            if arm=="B": messages=[messages[0]]+demonstrations+messages[1:]
            encoded=encode_answer(tokenizer,messages+[dict(role="assistant",content=answer)],request["id"]+"-"+arm,16134)
            encoded.update(task_id=request["id"],arm=arm)
            development.append(encoded)
    out.mkdir()
    for name,records in [("train",train),("development",development)]:
        (out/(name+".jsonl")).write_text("".join(json.dumps(r)+"\n" for r in records),encoding="utf-8")
    specials={token:tokenizer.convert_tokens_to_ids(token) for token in ["<|endoftext|>","<|im_start|>","<|im_end|>","<think>","</think>"]}
    config=json.loads((CHECKPOINT/"config.json").read_text())
    report={"status":"passed","base_revision":REV,"train_rows":60,"development_rows":len(development),"max_train_tokens":max(r["input_tokens"] for r in train),"max_development_tokens":max(r["input_tokens"] for r in development),"total_train_input_tokens":sum(r["input_tokens"] for r in train),"total_train_target_tokens":sum(r["target_tokens"] for r in train),"no_truncation":True,"prompt_and_empty_reasoning_markup_masked":True,"decoded_target_matches_every_answer":True,"policy":"Condition on the checkpoint's empty reasoning wrapper; supervise only authored visible assistant answer and im_end. Do not teach fabricated reasoning or supervise empty thinking decisions. This is answer-only SFT, not a guarantee of preserving thinking behavior.","historical_LM_Studio_settings":"unchanged; historical thinking-enabled controls remain separate","token_ids":specials,"model_config_eos":config["text_config"]["eos_token_id"],"generation_stop_policy":"Explicitly stop on im_end and endoftext; tokenizer EOS and model config EOS differ intentionally in the checkpoint.","train_jsonl_sha256":sha(out/"train.jsonl"),"development_jsonl_sha256":sha(out/"development.jsonl"),"source_export":provenance}
    (out/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    for record in [train[0],max(train,key=lambda r:r["input_tokens"])]:
        (out/(record["id"]+"-mask-review.txt")).write_text("MASKED PREFIX:\n"+tokenizer.decode(record["input_ids"][:record["first_target_token"]],skip_special_tokens=False)+"\n\nSUPERVISED ANSWER:\n"+tokenizer.decode([v for v in record["labels"] if v!=-100],skip_special_tokens=False)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="source_export"},indent=2))

if __name__=="__main__": main()
