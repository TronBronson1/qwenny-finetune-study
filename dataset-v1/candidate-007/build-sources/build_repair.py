"""CPU-only candidate-007 builder. Imports training/development definitions only."""
import sys
sys.dont_write_bytecode=True
import ast,builtins,copy,hashlib,importlib,json,pathlib,shutil,textwrap
HERE=pathlib.Path(__file__).resolve().parent
EXP=HERE.parents[1]; DATA=EXP/"dataset-v1"; OLD=DATA/"candidate-006"; OUT=DATA/"candidate-007"
sys.path.insert(0,str(OLD/"build-sources"))
import tasklib,tasks_training,tasks_development
sys.path.insert(0,str(HERE))
from repair_config import LABELS,VALID,INVALID,RETURNS
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,text): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding="utf-8",newline="\n")
def dump(p,value): write(p,json.dumps(value,indent=2,ensure_ascii=False)+"\n")
# Extract reusable original training/development assembly helpers; never import
# assemble.py, tasks_final.py, tasks_regression.py or their data.
wanted={"IntChild","StrChild","BytesChild","ListChild","TupleChild","DictChild","canonical","same","type_invalid","subtype_with_same_value","compile_function","build_cases","suite"}
tree=ast.parse((OLD/"build-sources/assemble.py").read_text(encoding="utf-8"))
nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in wanted or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="TEST_HEADER" for t in n.targets)]
ns=dict(copy=copy,builtins=builtins,tasklib=tasklib,textwrap=textwrap)
exec(compile(ast.Module(body=nodes,type_ignores=[]),"<selected-original-helpers>","exec"),ns)
original_type_invalid=ns["type_invalid"]
def type_invalid(schema,sample):
    values=original_type_invalid(schema,sample)
    I=ns["IntChild"]
    if schema=="ints": values += [["x"],[1.5],[-1.5],[None]]
    elif schema=="matrix": values += [[["x"]],[[1.5]],[[None]],[1]]
    elif schema=="pairs":
        values += [[1],[(True,1)],[(I(0),1)],[(0,I(1))],[("x",1)],[(0,"x")],[(1.5,2)],[(0,1.5)]]
    elif schema in ("pair","tuple3"):
        count=2 if schema=="pair" else 3
        for index in range(count):
            for wrong in ("x",1.5,None,True,I(0)):
                row=[0]*count; row[index]=wrong; values.append(tuple(row))
    return values
ns["type_invalid"]=type_invalid
# No 72-task return requires a dict; arbitrary rotated elements have their own
# identity tests. Keep recursive list/tuple checking, drop unrelated dict branch.
ns["TEST_HEADER"]=ns["TEST_HEADER"].split("    elif type(expected) is dict:")[0]
SYSTEM="Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution."
def call(source,name,args):
    fn=ns["compile_function"](source,name)
    try: return ("return",fn(*copy.deepcopy(args)))
    except Exception as error: return ("exception",type(error).__name__)
def same(a,b): return ns["same"](a,b)
def outcome_equal(a,b): return a[0]==b[0] and same(a[1],b[1])
def depth(v):
    if type(v) in (list,tuple): return 1+max((depth(x) for x in v),default=0)
    return 0
def requirement_witness(code,task,valid,invalid):
    for c in valid:
        args=copy.deepcopy(c["args"])
        try: result=ns["compile_function"](code,task.name)(*args)
        except Exception: continue
        if not same(result,c["expected"]) or not same(args,c["after"]):
            return dict(node=f'test_target.py::test_values[{c["id"]}]',case=c["id"],kind="result-or-post-state-assertion",args_python=repr(c["args"]),expected_python=repr(c["expected"]),actual_python=repr(result))
    for c in invalid:
        observed=call(code,task.name,c["args"])
        if observed[0]=="return":
            return dict(node=f'test_target.py::test_raises_{c["exception"].lower()}[{c["id"]}]',case=c["id"],kind="required-exception-not-raised",args_python=repr(c["args"]),expected_exception=c["exception"],actual_python=repr(observed[1]))
        if observed[1]!=c["exception"]:
            return dict(node=f'test_target.py::test_raises_{c["exception"].lower()}[{c["id"]}]',case=c["id"],kind="required-exception-wrong-class",args_python=repr(c["args"]),expected_exception=c["exception"],actual_exception=observed[1])
    return None
def wrapper(reference,name,body):
    return reference+"\n_original_function="+name+"\n"+body.replace("FUNCTION",name)+"\n"
def proposed_mutants(reference,task,record,valid):
    ident=record["id"]
    yield "return-exact-type",wrapper(reference,task.name,'''
class _ReturnInt(int): pass
class _ReturnStr(str): pass
class _ReturnList(list): pass
class _ReturnTuple(tuple): pass
def FUNCTION(*args):
    result=_original_function(*args)
    if type(result) is bool: return int(result)
    return {int:_ReturnInt,str:_ReturnStr,list:_ReturnList,tuple:_ReturnTuple}[type(result)](result)
''')
    if ident!="DV001" and any(depth(c["expected"])>=1 and c["expected"] for c in valid):
        yield "nested-return-exact-type",wrapper(reference,task.name,'''
class _ReturnInt(int): pass
class _ReturnStr(str): pass
def _corrupt_leaf(value):
    if type(value) is list: return [_corrupt_leaf(x) for x in value]
    if type(value) is tuple: return tuple(_corrupt_leaf(x) for x in value)
    if type(value) is bool: return int(value)
    if type(value) is int: return _ReturnInt(value)
    if type(value) is str: return _ReturnStr(value)
    return value
def FUNCTION(*args): return _corrupt_leaf(_original_function(*args))
''')
    if any(s in ("ints","strs","matrix","pairs","objects") for s in task.schemas):
        yield "valid-input-not-mutated",wrapper(reference,task.name,'''
def FUNCTION(*args):
    result=_original_function(*args)
    for arg in args:
        if type(arg) is list:
            arg.append("mutation-sentinel")
            break
        if type(arg) is tuple:
            for item in arg:
                if type(item) is list:
                    item.append("mutation-sentinel")
                    break
    return result
''')
    if any(s in ("ints","matrix","pairs","pair","tuple3") for s in task.schemas):
        mutated=reference.replace("_exact(item, int)","_ordinary_int_gap(item)")
        mutated+="\ndef _ordinary_int_gap(value):\n    if isinstance(value,int) and type(value) is not int: raise TypeError('int')\n"
        yield "ordinary-nested-int-rejection",mutated
    parsed=ast.parse(reference)
    function=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name==task.name)
    if len(function.body)>1 and isinstance(function.body[1],ast.If) and any(isinstance(n,ast.Raise) and isinstance(n.exc,ast.Call) and isinstance(n.exc.func,ast.Name) and n.exc.func.id in ("ValueError","IndexError") for n in ast.walk(function.body[1])):
        changed=copy.deepcopy(parsed); fn=next(n for n in changed.body if isinstance(n,ast.FunctionDef) and n.name==task.name)
        fn.body[0],fn.body[1]=fn.body[1],fn.body[0]
        yield "type-before-value-priority",ast.unparse(ast.fix_missing_locations(changed))+"\n"
    if any(isinstance(n,ast.Raise) and isinstance(n.exc,ast.Call) and isinstance(n.exc.func,ast.Name) and n.exc.func.id=="IndexError" for n in ast.walk(function)):
        changed=copy.deepcopy(parsed); fn=next(n for n in changed.body if isinstance(n,ast.FunctionDef) and n.name==task.name)
        for n in ast.walk(fn):
            if isinstance(n,ast.Raise) and isinstance(n.exc,ast.Call) and isinstance(n.exc.func,ast.Name) and n.exc.func.id=="IndexError": n.exc.func.id="ValueError"
        yield "bounds-exception-class",ast.unparse(ast.fix_missing_locations(changed))+"\n"
    if ident=="TR031": yield "left-input-order",wrapper(reference,task.name,"def FUNCTION(*args): return sorted(_original_function(*args))")
    if ident=="TR032": yield "stable-positive-order",wrapper(reference,task.name,"def FUNCTION(*args):\n    a,b,c=_original_function(*args)\n    return a,b,sorted(c)")
    if ident=="DV007":
        changed=reference.replace("rows <= 0 or columns <= 0","rows <= 0")
        if changed!=reference: yield "positive-columns",changed
        yield "neighbor-order",wrapper(reference,task.name,"def FUNCTION(*args): return list(reversed(_original_function(*args)))")
    if ident=="DV011":
        changed=reference.replace("low > result[-1][1]","low >= result[-1][1]")
        if changed!=reference: yield "touching-intervals-merge",changed
    external=EXP/"program/reviews/review-002/rubric_mutants"/(record["split"]+"_"+ident)/"rubric_mutant/subject.py"
    if external.exists(): yield "external-adversarial-witness",external.read_text(encoding="utf-8")
    # Extend digit-normalization witnesses to the other explicit ASCII parsers.
    if ident in ("TR037","TR041","TR042","TR046","TR057","DV002"):
        changed=ast.parse(reference); fn=next(n for n in changed.body if isinstance(n,ast.FunctionDef) and n.name==task.name)
        for node in ast.walk(fn):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=="re" and node.func.attr=="fullmatch" and len(node.args)>=2:
                operand=ast.unparse(node.args[1])
                node.args[1]=ast.parse("''.join(str(int(c)) if c.isdecimal() else c for c in "+operand+")",mode="eval").body
        yield "ascii-digit-boundary",ast.unparse(ast.fix_missing_locations(changed))+"\n"

def main():
    assert not OUT.exists(),"Refuse to overwrite any previous candidate"
    artifacts={}; reports=[]; proposals=[]
    for split in ("training","development"):
        for original in sorted((OLD/"tasks"/split).iterdir()):
            record=json.loads((original/"record.json").read_text(encoding="utf-8"))
            ident=record["id"]; task=copy.deepcopy(tasklib.TASKS[record["function"]])
            reference=(original/"evaluator/reference/subject.py").read_text(encoding="utf-8")
            assert reference==tasklib.source(task),(ident,"reference/source mismatch")
            labels=LABELS[ident].split("|"); assert len(labels)==len(task.inputs),(ident,labels,task.inputs)
            for args,label in VALID.get(ident,[]): task.inputs.append(args); labels.append(label)
            task.invalid.extend((args,error) for args,error,label in INVALID.get(ident,[]))
            if "tuple3" in task.schemas:
                for position,schema in enumerate(task.schemas):
                    if schema!="tuple3": continue
                    for component in range(3):
                        args=list(copy.deepcopy(task.inputs[0])); row=[0,0,0]; row[component]=-1; args[position]=tuple(row); task.invalid.append((tuple(args),"ValueError"))
            fn=ns["compile_function"](reference,task.name)
            valid,invalid,checks=ns["build_cases"](task,fn)
            assert len(valid)==len(labels)
            target=ns["suite"](task,valid,invalid)
            mutable=any(s not in ("int","str","bytes") for s in task.schemas)
            if not mutable:
                target=target.replace("    before=copy.deepcopy(args)\n","").replace("    assert args == before\n","")
                if "copy." not in target: target=target.replace("import copy\n","")
            compile(target,"<repaired-gold>","exec")
            body=task.contract
            for phrase in (" Do not mutate the input."," Do not mutate input."," Do not mutate either input."," Do not mutate tokens."): body=body.replace(phrase,"")
            if ident=="TR041": body=body.replace("signed canonical decimal integers","signed canonical ASCII decimal integers")
            if ident=="TR047": body=body.replace("Return the start index","Matches are literal and case-sensitive. Return the start index")
            schema_text={
                "int":"exact built-in int; reject bool and int subclasses",
                "str":"exact built-in str; reject str subclasses",
                "bytes":"exact built-in bytes; reject subclasses",
                "ints":"exact list of exact ints; reject bool, int subclasses and list subclasses",
                "strs":"exact list of exact strings; reject list and str subclasses",
                "matrix":"exact list of exact lists of exact ints; reject bool and subclasses at all stated levels",
                "pairs":"exact list of exact two-item tuples of exact ints; reject bool and list/tuple/int subclasses",
                "tuple3":"exact three-item tuple of exact ints; reject bool and tuple/int subclasses",
                "objects":"exact tuple of arbitrary objects; reject tuple subclasses"
            }
            parts=[f"Function contract: {task.name}({', '.join(task.params)})."]
            parts += [f"- {p}: {schema_text[s]}." for p,s in zip(task.params,task.schemas)]
            parts += ["Reject invalid specified types with TypeError before shape/value checks.",body,"Return type: "+RETURNS[ident]+"."]
            if mutable: parts.append("Do not mutate any input or nested mutable elements.")
            coverage="Coverage expectations: include normal cases for "+", ".join(labels)+". Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels."
            if mutable: coverage+=" Compare valid inputs before and after calls."
            parts += [coverage,f"Write one complete pytest file importing 'from subject import {task.name}'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution."]
            spec="\n\n".join(parts)+"\n"
            mapping="; ".join(f"{label}={c['id']}" for label,c in zip(labels,valid))
            groups={exc:[c["id"] for c in invalid if c["exception"]==exc] for exc in sorted({c["exception"] for c in invalid})}
            prose=f"Return cases: {mapping}. Validation cases: "+ "; ".join(exc+"="+",".join(ids) for exc,ids in groups.items())+". Exact returned types are checked recursively where specified."
            if mutable: prose+=" Valid-input preservation is checked before/after calls."
            prose+=" These finite witnesses do not prove exhaustive correctness. No execution is claimed."
            fence=chr(96)*3
            answer=fence+"python\n"+target+fence+"\n\n"+prose+"\n"
            cases=[dict(id=c["id"],args_python=repr(c["args"]),expected_python=repr(c["expected"]),after_python=repr(c["after"]),category=label) for c,label in zip(valid,labels)]
            cases += [dict(id=c["id"],args_python=repr(c["args"]),exception=c["exception"],category=c["category"]) for c in invalid]
            mutants=[]
            for old in json.loads((original/"evaluator/mutants.json").read_text(encoding="utf-8")):
                source=(original/"evaluator/mutants"/old["id"]/"subject.py").read_text(encoding="utf-8")
                witness=requirement_witness(source,task,valid,invalid)
                assert witness,(ident,old["id"],"lost original witness")
                mutants.append(dict(id=old["id"],requirement="legacy-"+old["defect"],source=source,witness=witness,provenance="unchanged candidate-006 mutant; witness refreshed against revised gold"))
            seen={hashlib.sha256(m["source"].encode()).hexdigest() for m in mutants}
            for label,source in proposed_mutants(reference,task,record,valid):
                compile(source,"<proposed-requirement-mutant>","exec")
                digest=hashlib.sha256(source.encode()).hexdigest()
                if digest in seen: continue
                witness=requirement_witness(source,task,valid,invalid)
                proposals.append(dict(task=ident,requirement=label,status="designated" if witness else "no-relevant-finite-witness",witness=witness))
                if not witness: continue
                seen.add(digest); mutants.append(dict(id=f"R{len(mutants)-2:02}",requirement=label,source=source,witness=witness,provenance="S007 requirement-linked fixture; finite witness validated against unchanged reference"))
            new_record={**record,"revision":2,"status":"repair-candidate-unapproved","review_status":"finite-agent-calibration-pending-execution","training_eligible":False,"parent_candidate":"candidate-006","source_sha256":hashlib.sha256(reference.encode()).hexdigest(),"spec_sha256":hashlib.sha256(spec.encode()).hexdigest(),"target_sha256":hashlib.sha256(target.encode()).hexdigest(),"answer_sha256":hashlib.sha256(answer.encode()).hexdigest(),"valid_test_cases":len(valid),"exception_test_cases":len(invalid),"designated_mutants":len(mutants)}
            rubric=dict(status="finite-agent-reviewed-category-map-pending-execution",model_visible=True,return_type=RETURNS[ident],semantic_categories=[dict(requirement=label,gold_case=c["id"]) for label,c in zip(labels,valid)],type_coverage="Every stated argument/type level: ordinary and subclass; bool for int; other arguments valid.",validation_order="Type checks before value/shape; stated shape checks before bounds.",mutation_applicable=mutable,limitations="Finite same-agent semantic review. External semantic review covers eight S006 tasks only; this is not independent review of all72.")
            report=dict(id=ident,split=split,source_reference_unchanged=True,source_hash=new_record["source_sha256"],valid_cases=len(valid),invalid_cases=len(invalid),oracle_checks=checks,semantic_categories=labels,mutants=len(mutants),review="Agent read original contract and valid-case table; added finite witnesses for observed semantic/type gaps. External eight-task findings corroborated separately.")
            artifacts[ident]=dict(split=split,record=new_record,reference=reference,target=target,answer=answer,spec=spec,cases=cases,mutants=mutants,rubric=rubric,messages=[dict(role="system",content=SYSTEM),dict(role="user",content=spec)])
            reports.append(report)
    assert len(artifacts)==72
    OUT.mkdir()
    for ident,a in artifacts.items():
        folder=OUT/"tasks"/a["split"]/ident
        write(folder/"SPEC.md",a["spec"]); write(folder/"PROMPT.md",SYSTEM+"\n\n"+a["spec"]); write(folder/"TARGET.md",a["answer"]); write(folder/"test_target.py",a["target"])
        dump(folder/"record.json",a["record"]); dump(folder/"rubric.json",a["rubric"]); dump(folder/"evaluator/cases.json",a["cases"]); write(folder/"evaluator/reference/subject.py",a["reference"])
        manifest=[]
        for mutant in a["mutants"]:
            write(folder/"evaluator/mutants"/mutant["id"]/"subject.py",mutant["source"])
            manifest.append({k:v for k,v in mutant.items() if k!="source"}|dict(source_sha256=hashlib.sha256(mutant["source"].encode()).hexdigest()))
        dump(folder/"evaluator/mutants.json",manifest)
        for name in ("oracle.py","oracle-inputs.json","oracle-check.json"):
            shutil.copyfile(OLD/"tasks"/a["split"]/ident/"evaluator"/name,folder/"evaluator"/name)
    for split in ("training","development"):
        packets=[dict(id=i,family=a["record"]["family"],messages=a["messages"]+([dict(role="assistant",content=a["answer"])] if split=="training" else [])) for i,a in artifacts.items() if a["split"]==split]
        write(OUT/"model-packets"/(split+"-requests.jsonl"),"\n".join(json.dumps(p,ensure_ascii=False) for p in packets)+"\n")
    for p in (pathlib.Path(__file__),HERE/"repair_config.py",HERE/"PROTOCOL.md"):
        shutil.copyfile(p,OUT/"build-sources"/p.name) if (OUT/"build-sources").exists() else None
    (OUT/"build-sources").mkdir(exist_ok=True)
    for p in (pathlib.Path(__file__),HERE/"repair_config.py",HERE/"PROTOCOL.md"): shutil.copyfile(p,OUT/"build-sources"/p.name)
    dump(OUT/"manifest.json",dict(candidate="candidate-007",scope="training/development only; final/regression omitted and untouched",parent="candidate-006",status="pending-calibration-validation",training_authorization="not exported or approved under prior corpus hash",tasks=[a["record"] for a in artifacts.values()]))
    dump(OUT/"calibration-design.json",dict(tasks=reports,proposed_mutants=proposals,review_limit="same coordinating agent; no newly claimed independent72-task semantic review"))
    write(OUT/"README.md","# Candidate007 — calibration repair\n\nTraining/development-only derivative:60 training and12 development tasks. Final/regression tasks are deliberately omitted; original candidate006 remains intact. No training export or approval is implied. See manifest.json and calibration-design.json; execution validation is pending.\n")
    hashes={p.relative_to(OUT).as_posix():sha(p) for p in OUT.rglob("*") if p.is_file()}
    dump(OUT/"SHA256.json",hashes)
    dump(HERE/"build-report.json",dict(status="built-pending-execution",tasks=reports,source_hash_manifest_sha256=sha(OUT/"SHA256.json"),designated_mutants=sum(x["mutants"] for x in reports),oracle_checks=sum(x["oracle_checks"] for x in reports),proposals=proposals))
    print(json.dumps(dict(tasks=len(reports),mutants=sum(x["mutants"] for x in reports),oracle_checks=sum(x["oracle_checks"] for x in reports)),indent=2))
if __name__=="__main__": main()

