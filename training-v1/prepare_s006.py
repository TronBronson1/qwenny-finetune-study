"""Select diagnostic tasks from declared metadata only, without final/regression access."""
import hashlib,json,pathlib
from runtime import ROOT,EXP,tokenizer

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8")
def main():
    study=EXP/"studies/S006-learning-and-transfer"
    destination=study/"selection.json"
    assert not destination.exists()
    corpus=EXP/"dataset-v1/candidate-006"
    tok=tokenizer()
    prepared={}
    for name in ("train","development"):
        for line in (ROOT/"prepared-001"/(name+".jsonl")).read_text(encoding="utf-8").splitlines():
            item=json.loads(line)
            if item["id"].endswith("-B"): continue
            prepared[item["id"].removesuffix("-A")]=item
    train=[json.loads(x) for x in (corpus/"training-candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    dev=[json.loads(x) for x in (corpus/"model-packets/development-requests.jsonl").read_text(encoding="utf-8").splitlines()]
    packets={x["id"]:x for x in train+dev}
    selected=[]; pools={}
    for split,prefix in (("training","TR"),("development","DV")):
        rows=[]
        for task in sorted((corpus/"tasks"/split).iterdir()):
            if not task.is_dir(): continue
            record=json.loads((task/"record.json").read_text(encoding="utf-8"))
            ident=record["id"]; assert ident.startswith(prefix)
            if ident in ("DV001","DV002"): continue
            rows.append(dict(id=ident,family=record["family"],split=split,target_tokens=prepared[ident]["target_tokens"],schemas=record["schemas"],function=record["function"]))
        # Deduplicate families by lowest ID, then span target-length range.
        unique={}
        for row in sorted(rows,key=lambda x:x["id"]): unique.setdefault(row["family"],row)
        ordered=sorted(unique.values(),key=lambda x:(x["target_tokens"],x["id"]))
        indices=[0,(len(ordered)-1)//3,2*(len(ordered)-1)//3,len(ordered)-1]
        assert len(set(indices))==4
        pools[split]=dict(eligible=ordered,selected_indices=indices)
        for index in indices:
            row=ordered[index]; item=packets[row["id"]]
            messages=[m for m in item["messages"] if m["role"]!="assistant"]
            assert [m["role"] for m in messages]==["system","user"]
            prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
            ids=tok(prompt,add_special_tokens=False)["input_ids"]
            assert len(ids)+2048<=16134
            assert row["target_tokens"]<2048
            folder=study/"inputs"/row["id"]; folder.mkdir(parents=True,exist_ok=True)
            write(folder/"messages.json",messages)
            write(folder/"prompt-token-ids.json",ids)
            (folder/"prompt.txt").write_text(prompt,encoding="utf-8")
            row.update(prompt_tokens=len(ids),messages_sha256=sha(folder/"messages.json"),prompt_sha256=sha(folder/"prompt.txt"),prompt_ids_sha256=sha(folder/"prompt-token-ids.json"))
            if split=="training":
                original=item["messages"]
                assert original[-1]["role"]=="assistant"
                row["matches_original_training_messages"]=messages==original[:-1]
                assert row["matches_original_training_messages"]
            selected.append(row)
    result=dict(status="selected-before-generation",rule="Exclude DV001/DV002; one lowest-ID representative per family; sort by supervised target token count then ID; choose indices 0, floor((n-1)/3), floor(2*(n-1)/3), n-1 independently per split.",limits="Length-spanning purposive sample, not random or category-balanced. Schemas reported for audit; no representativeness claim. Development targets already used for loss.",pools=pools,tasks=selected)
    write(destination,result)
    print(json.dumps(selected,indent=2))
if __name__=="__main__": main()
