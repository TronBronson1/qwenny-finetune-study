"""Pinned tokenizer-only profile; does not load model weights or touch CUDA."""
import sys,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]
sys.path.insert(0,str(EXP/"training-v1"))
from runtime import tokenizer
def main():
    out=HERE/"token-profile.json"; assert not out.exists()
    tok=tokenizer(); rows=[]
    for line in (EXP/"dataset-v1/candidate-007/model-packets/training-requests.jsonl").read_text(encoding="utf-8").splitlines():
        row=json.loads(line)
        text=tok.apply_chat_template(row["messages"],tokenize=False,add_generation_prompt=False,enable_thinking=False)
        length=len(tok(text,add_special_tokens=False)["input_ids"])
        answer=len(tok(row["messages"][-1]["content"],add_special_tokens=False)["input_ids"])
        rows.append(dict(id=row["id"],complete_chat_tokens=length,plain_assistant_text_tokens=answer))
    report=dict(scope="CPU tokenizer profile only; not loss-mask validation, training export, GPU fit or instruction-following evidence.",maximum_chat_tokens=max(x["complete_chat_tokens"] for x in rows),maximum_plain_answer_tokens=max(x["plain_assistant_text_tokens"] for x in rows),over_previous_2048_chat_budget=[x["id"] for x in rows if x["complete_chat_tokens"]>2048],rows=rows)
    out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print(json.dumps({k:v for k,v in report.items() if k!="rows"},indent=2))
if __name__=="__main__": main()

