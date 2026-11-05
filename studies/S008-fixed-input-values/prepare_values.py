"""Prepare fixed input values without leaking gold answers into model prompts."""
import ast,copy,hashlib,json,pathlib,runpy,sys,time
HERE=pathlib.Path(__file__).resolve().parent; EXP=HERE.parents[1]; DATA=EXP/"dataset-v1/candidate-007"
sys.path.insert(0,str(EXP/"training-v1"))
from runtime import tokenizer
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding="utf-8")
def normalize(x): return json.loads(json.dumps(x,ensure_ascii=False))
def main():
    assert not (HERE/"freeze-manifest.json").exists()
    certificate=json.loads((EXP/"studies/S007-measurement-repair/calibration-certificate.json").read_text(encoding="utf-8"))
    assert certificate["status"]=="passed" and certificate["final_candidate_hash"]==sha(DATA/"SHA256.json")
    for name,digest in json.loads((DATA/"SHA256.json").read_text(encoding="utf-8")).items(): assert sha(DATA/name)==digest,name
    tok=tokenizer(); tasks=[]
    for split,ids in (("training",("TR024","TR025","TR038","TR049")),("development",("DV008","DV004","DV011","DV007"))):
        for ident in ids:
            folder=DATA/"tasks"/split/ident
            record=json.loads((folder/"record.json").read_text(encoding="utf-8"))
            cases=[c for c in json.loads((folder/"evaluator/cases.json").read_text(encoding="utf-8")) if "expected_python" in c]
            indices=[0,(len(cases)-1)//3,2*(len(cases)-1)//3,len(cases)-1]; assert len(set(indices))==4
            chosen=[cases[i] for i in indices]
            ref=runpy.run_path(str(folder/"evaluator/reference/subject.py"))[record["function"]]
            oracle=runpy.run_path(str(folder/"evaluator/oracle.py"))["oracle"]
            expected=[]
            for case in chosen:
                args=ast.literal_eval(case["args_python"]); value=ast.literal_eval(case["expected_python"])
                assert normalize(ref(*copy.deepcopy(args)))==normalize(oracle(*copy.deepcopy(args)))==normalize(value)
                expected.append(normalize(value))
            contract=(folder/"SPEC.md").read_text(encoding="utf-8").split("Coverage expectations:")[0].strip()
            request=contract+"\n\nCalculate the four return values for these argument tuples, in this order:\n"
            request+="\n".join(f"{i+1}. {c['args_python']}" for i,c in enumerate(chosen))
            request+="\n\nReturn only one JSON array with exactly four entries, one return value per call. Represent tuples as JSON arrays, including nested tuples. Preserve strings and numbers. Do not write tests, code, reasoning, explanations or a code fence."
            messages=[dict(role="system",content="Calculate return values from the supplied contract and explicit inputs. Return only the requested JSON array."),dict(role="user",content=request)]
            prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
            ids_tokens=tok(prompt,add_special_tokens=False)["input_ids"]; assert len(ids_tokens)+512<=16134
            input_folder=HERE/"inputs"/ident; input_folder.mkdir(parents=True,exist_ok=False)
            write(input_folder/"messages.json",messages); write(input_folder/"prompt-token-ids.json",ids_tokens); (input_folder/"prompt.txt").write_text(prompt,encoding="utf-8")
            write(HERE/"expected"/(ident+".json"),dict(task=ident,case_ids=[c["id"] for c in chosen],args_python=[c["args_python"] for c in chosen],values=expected,reference_and_oracle_agree=True))
            tasks.append(dict(id=ident,split=split,family=record["family"],case_indices=indices,case_ids=[c["id"] for c in chosen],prompt_tokens=len(ids_tokens),prompt_ids_sha256=sha(input_folder/"prompt-token-ids.json"),reference_sha256=sha(folder/"evaluator/reference/subject.py"),oracle_sha256=sha(folder/"evaluator/oracle.py")))
    write(HERE/"selection.json",dict(status="selected-before-generation",tasks=tasks,scope="Fixed-input component diagnostic; same eight visible task IDs; no test generation or optimizer updates."))
    files={}
    for path in [HERE/"PROTOCOL.md",pathlib.Path(__file__),EXP/"training-v1/s008_probe.py",HERE/"score_values.py",EXP/"training-v1/runtime.py",DATA/"SHA256.json",EXP/"studies/S007-measurement-repair/calibration-certificate.json",HERE/"selection.json"]:
        files[path.relative_to(EXP).as_posix()]=sha(path)
    for root in (HERE/"inputs",HERE/"expected"):
        for path in root.rglob("*"):
            if path.is_file(): files[path.relative_to(EXP).as_posix()]=sha(path)
    for epoch in (1,5):
        for name in ("adapter_model.safetensors","adapter_config.json","reload-probe.pt"):
            path=EXP/"training-v1/runs/qwenny-001/checkpoints"/f"epoch-{epoch}"/name; files[path.relative_to(EXP).as_posix()]=sha(path)
    write(HERE/"freeze-manifest.json",dict(status="frozen-before-generation",unix_time=time.time(),files=files,review="Coordinating-agent design review; calibration gate passed; no new independent semantic review claimed."))
    print(json.dumps(dict(tasks=8,cases=32,arms=3,files_frozen=len(files),max_prompt_tokens=max(t["prompt_tokens"] for t in tasks)),indent=2))
if __name__=="__main__": main()

