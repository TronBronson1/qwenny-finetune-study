"""Mechanical split/leakage and normalized-source-clone audit; not semantic review."""
import argparse, ast, collections, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(); p.add_argument("dataset"); p.add_argument("--out",required=True); a=p.parse_args()
    root=ROOT/a.dataset; output=ROOT/a.out
    assert not output.exists()
    manifest=json.loads((root/"manifest.json").read_text(encoding="utf-8")); records=manifest["tasks"]
    counts=collections.Counter(r["split"] for r in records)
    assert counts=={"training":60,"development":12,"final":24,"regression":12}
    assert len({r["id"] for r in records})==108
    splits={}
    for record in records: splits.setdefault(record["family"],set()).add(record["split"])
    assert all(len(s)==1 for s in splits.values())
    for split in ("training","development","final","regression"):
        file=root/"training-candidates.jsonl" if split=="training" else root/"model-packets"/(split+"-requests.jsonl")
        rows=[json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()]
        assert {r["id"] for r in rows}=={r["id"] for r in records if r["split"]==split}
        for row in rows:
            roles=[m["role"] for m in row["messages"]]
            if split=="training": assert roles==["system","user","assistant"]
            else: assert "assistant" not in roles
    signatures=[]
    for record in records:
        if record["kind"]=="explanation": continue
        folder=root/"tasks"/record["split"]/record["id"]
        target=ast.parse((folder/"test_target.py").read_text(encoding="utf-8"))
        assert not any(isinstance(n,ast.FunctionDef) and n.name==record["function"] for n in ast.walk(target))
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ("eval","exec","open","__import__") for n in ast.walk(target))
        tree=ast.parse((folder/"evaluator"/"reference"/"subject.py").read_text(encoding="utf-8"))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==record["function"])
        fn.body=fn.body[1:]  # Strip the common type-validation prelude.
        names={v.arg:f"arg{i}" for i,v in enumerate(fn.args.args)}
        for n in ast.walk(fn):
            if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id not in names: names[n.id]=f"local{len(names)}"
        class Normalize(ast.NodeTransformer):
            def visit_Name(self,n): return ast.copy_location(ast.Name(id=names.get(n.id,n.id),ctx=n.ctx),n)
            def visit_arg(self,n): n.arg=names.get(n.arg,n.arg); return n
            def visit_Constant(self,n): return ast.copy_location(ast.Constant(value=f"<{type(n.value).__name__}>"),n)
        fn=Normalize().visit(fn); fn.name="FUNCTION"
        signatures.append(dict(id=record["id"],split=record["split"],signature=hashlib.sha256(ast.dump(fn,include_attributes=False).encode()).hexdigest()))
    groups=collections.defaultdict(list)
    for row in signatures: groups[row["signature"]].append(row)
    clones=[g for g in groups.values() if len({r["split"] for r in g})>1]
    assert not clones,clones
    report={"status":"passed","dataset":a.dataset,"dataset_hash_manifest_sha256":hashlib.sha256((root/"SHA256.json").read_bytes()).hexdigest(),"split_counts":dict(counts),"declared_families":len(splits),"family_ids_crossing_splits":0,"normalized_cross_split_source_clones":clones,"model_packet_answers_outside_training":0,"reference_targets_checked":len(signatures),"limitation":"No exact normalized clone does not establish semantic independence. The human family/split audit and every target review remain pending."}
    output.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__": main()
