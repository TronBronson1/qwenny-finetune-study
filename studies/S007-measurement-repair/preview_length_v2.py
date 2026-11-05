"""Presentation-only TR058 length preview; all executable AST retained except IDs."""
import ast,copy,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]
sys.path.insert(0,str(EXP/"training-v1"))
from runtime import tokenizer
def normalized(text):
    tree=ast.parse(text)
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="pytest" and n.func.attr=="param": n.keywords=[k for k in n.keywords if k.arg!="id"]
    return ast.dump(tree,include_attributes=False)
def main():
    out=HERE/"length-preview-002"; assert not out.exists(); out.mkdir()
    task=EXP/"dataset-v1/candidate-007/tasks/training/TR058"
    original=(task/"test_target.py").read_text(encoding="utf-8")
    compact=re.sub(r''',\s*id\s*=\s*(['"])[^'"\n]*\1''',"",original)
    compact="\n".join(line.rstrip() for line in compact.splitlines() if line.strip())+"\n"
    compact=re.sub(r", +",",",compact)
    assert normalized(original)==normalized(compact)
    prose="Equal versions return 0; (1,2,3)/(1,2,4) returns -1; (1,3,0)/(1,2,99) and (2,0,0)/(1,99,99) return 1. TypeError cases isolate ordinary wrong types, bool and subclasses at the stated argument/component levels, including type-before-value witnesses. ValueError cases cover tuple shape and negative components. Exact int return is checked. Finite cases are not exhaustive. No execution is claimed."
    fence=chr(96)*3
    answer=fence+"python\n"+compact+fence+"\n\n"+prose+"\n"
    row=next(json.loads(x) for x in (EXP/"dataset-v1/candidate-007/model-packets/training-requests.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(x)["id"]=="TR058")
    original_messages=copy.deepcopy(row["messages"]); messages=copy.deepcopy(original_messages); messages[-1]["content"]=answer
    tok=tokenizer()
    def count(m): return len(tok(tok.apply_chat_template(m,tokenize=False,add_generation_prompt=False,enable_thinking=False),add_special_tokens=False)["input_ids"])
    report=dict(status="presentation-preview-only",task="TR058",source="candidate-007",original_chat_tokens=count(original_messages),preview_chat_tokens=count(messages),within_previous2048=count(messages)<=2048,executable_ast_equal_ignoring_display_ids=True,limitations="Not a new approved training export. Same cases, assertions and runtime behavior; prose shortened to concrete mappings and pytest display IDs removed.")
    (out/"test_target.py").write_text(compact,encoding="utf-8")
    (out/"TARGET.md").write_text(answer,encoding="utf-8")
    (out/"messages.json").write_text(json.dumps(messages,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"profile.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()

