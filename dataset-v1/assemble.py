"""Assemble a fresh, review-gated dataset candidate without training any model."""
import argparse, ast, builtins, copy, hashlib, json, pathlib, textwrap, sys
import tasklib
import tasks_training, tasks_development, tasks_final, tasks_regression
from tasks_regression import EXPLANATIONS

ROOT=pathlib.Path(__file__).resolve().parent
FENCE=chr(96)*3

class IntChild(int):
    def __repr__(self): return f"IntChild({int(self)!r})"
class StrChild(str):
    def __repr__(self): return f"StrChild({str(self)!r})"
class BytesChild(bytes):
    def __repr__(self): return f"BytesChild({bytes(self)!r})"
class ListChild(list):
    def __repr__(self): return f"ListChild({list(self)!r})"
class TupleChild(tuple):
    def __repr__(self): return f"TupleChild({tuple(self)!r})"
class DictChild(dict):
    def __repr__(self): return f"DictChild({dict(self)!r})"

def sha(data): return hashlib.sha256(data).hexdigest()
def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8",newline="\n")
def dump(path,value): write(path,json.dumps(value,indent=2,ensure_ascii=False)+"\n")

def canonical(value):
    if type(value) is dict: return {k:canonical(value[k]) for k in sorted(value,key=repr)}
    if type(value) is list: return [canonical(x) for x in value]
    if type(value) is tuple: return tuple(canonical(x) for x in value)
    return value

def same(left,right):
    if type(left) is not type(right): return False
    if isinstance(left,(list,tuple)): return len(left)==len(right) and all(same(a,b) for a,b in zip(left,right))
    if type(left) is dict: return left.keys()==right.keys() and all(same(left[k],right[k]) for k in left)
    return left==right

def type_invalid(schema,sample):
    if schema=="int": return [True,IntChild(sample),1.5,"bad",None]
    if schema=="str": return [StrChild(sample),b"x",1,None]
    if schema=="bytes": return [BytesChild(sample),bytearray(sample),"x",None]
    if schema=="ints": return [ListChild(sample),[True],[IntChild(1)],(),None]
    if schema=="strs": return [ListChild(sample),[StrChild("x")],[1],(),None]
    if schema=="matrix": return [ListChild(sample),[ListChild([1])],[[True]],[[IntChild(1)]],["x"],None]
    if schema in ("pair","tuple3"):
        count=2 if schema=="pair" else 3
        return [TupleChild(sample),tuple([True]+[0]*(count-1)),tuple([IntChild(1)]+[0]*(count-1)),list(sample),None]
    if schema=="objects": return [TupleChild(sample),list(sample),None]
    if schema=="pairs": return [ListChild(sample),[TupleChild((0,1))],[(0,True)],[(0,"x")],None]
    if schema=="commands": return [ListChild(sample),[["get","a"]],None]
    if schema=="counts": return [DictChild(sample),{1:2},{"x":True},{"x":IntChild(1)},None]
    if schema=="aliases": return [DictChild(sample),{1:"x"},{"x":1},None]
    if schema=="maybe_strs": return [ListChild([]),[StrChild("x")],[1],(),1]
    if schema=="stream": return [1,"x",{},[True],[IntChild(1)]]
    raise AssertionError(schema)

def subtype_with_same_value(schema,value):
    """Retain the invalid value while adding an exact-type violation."""
    if schema=="int" and type(value) is int: return IntChild(value)
    if schema=="str" and type(value) is str: return StrChild(value)
    if schema=="bytes" and type(value) is bytes: return BytesChild(value)
    if schema in ("ints","strs","matrix","pairs","commands","maybe_strs","stream") and type(value) is list: return ListChild(value)
    if schema in ("pair","tuple3","objects","stream") and type(value) is tuple: return TupleChild(value)
    if schema in ("counts","aliases") and type(value) is dict: return DictChild(value)
    raise ValueError("No appropriate subclass witness")

SCHEMA_TEXT={
    "int":"an exact built-in int (reject bool and subclasses)",
    "str":"an exact built-in str (reject subclasses)",
    "bytes":"an exact built-in bytes (reject subclasses and bytearray)",
    "ints":"an exact list of exact ints (reject bool, subclasses and list subclasses)",
    "strs":"an exact list of exact strings (reject subclasses at both levels)",
    "matrix":"an exact list of exact lists of exact ints (reject bool and subclasses)",
    "pair":"an exact tuple of exactly two exact ints",
    "tuple3":"an exact tuple of exactly three exact ints",
    "objects":"an exact tuple (arbitrary elements; reject tuple subclasses)",
    "pairs":"an exact list of exact two-int tuples",
    "commands":"an exact list of exact tuples (further command-element rules below)",
    "counts":"an exact dict with exact str keys and exact int values",
    "aliases":"an exact dict with exact str keys and exact str values",
    "maybe_strs":"None or an exact list of exact strings",
    "stream":"an exact list, exact tuple, or generator (further element rules below)"
}

def compile_function(source,name):
    ns={}
    exec(compile(source,"<original-local-fixture>","exec"),ns)
    return ns[name]

def build_cases(task,reference):
    oracle=tasklib.oracle_function(task)
    valid=[]; checks=0
    for number,args in enumerate(task.inputs):
        oracle_args=copy.deepcopy(args)
        expected=oracle(*oracle_args)
        ref_args=copy.deepcopy(args)
        actual=reference(*ref_args)
        assert same(actual,expected),(task.name,args,actual,expected)
        if task.mutates: assert same(ref_args,oracle_args),(task.name,"oracle post-state")
        else: assert same(ref_args,args),(task.name,"unexpected mutation")
        valid.append(dict(id=f"v{number:03}",args=copy.deepcopy(args),expected=canonical(expected),after=canonical(oracle_args)))
        checks+=1
    for args in task.extra:
        a=copy.deepcopy(args); b=copy.deepcopy(args)
        result=reference(*a); expected=oracle(*b)
        assert same(result,expected),(task.name,"bounded oracle",args,result,expected)
        assert same(a,b) if task.mutates else same(a,args)
        checks+=1
    invalid=[]
    for index,schema in enumerate(task.schemas):
        for bad in type_invalid(schema,task.inputs[0][index]):
            args=list(copy.deepcopy(task.inputs[0])); args[index]=bad
            invalid.append(dict(args=tuple(args),exception="TypeError",category=f"type:{task.params[index]}"))
    for args,error in task.invalid:
        invalid.append(dict(args=copy.deepcopy(args),exception=error,category="explicit-invalid"))
    # Preserve each invalid value and add an exact-type violation. This also
    # distinguishes type-before-value behavior for single-argument parsers.
    for args,error in task.invalid:
        if error=="TypeError": continue
        for index,schema in enumerate(task.schemas):
            try: bad=subtype_with_same_value(schema,args[index])
            except ValueError: continue
            mixed=list(copy.deepcopy(args)); mixed[index]=bad
            invalid.append(dict(args=tuple(mixed),exception="TypeError",category="type-before-value"))
    seen=set(); unique=[]
    for case in invalid:
        key=(repr(case["args"]),case["exception"])
        if key in seen: continue
        seen.add(key); case["id"]=f"e{len(unique):03}"
        try: reference(*copy.deepcopy(case["args"]))
        except Exception as e:
            assert isinstance(e,getattr(builtins,case["exception"])),(task.name,case,type(e).__name__)
        else: raise AssertionError((task.name,"invalid case did not raise",case))
        unique.append(case)
    return valid,unique,checks

TEST_HEADER='''import copy
import pytest
from subject import {function}

class IntChild(int): pass
class StrChild(str): pass
class BytesChild(bytes): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])
'''

def suite(task,valid,invalid):
    text=TEST_HEADER.format(function=task.name)
    used="\n".join(repr(c["args"]) for c in invalid)
    for name,kind in [("IntChild","int"),("StrChild","str"),("BytesChild","bytes"),("ListChild","list"),("TupleChild","tuple"),("DictChild","dict")]:
        if name not in used: text=text.replace(f"class {name}({kind}): pass\n","")
    parameters="args,expected,after" if task.mutates else "args,expected"
    text+=f'\n@pytest.mark.parametrize("{parameters}", [\n'
    for c in valid:
        after=f', {c["after"]!r}' if task.mutates else ""
        text+=f'    pytest.param({c["args"]!r}, {c["expected"]!r}{after}, id="{c["id"]}"),\n'
    text+=f'])\ndef test_values({parameters}):\n'
    text+='    before=copy.deepcopy(args)\n'
    text+=f'    actual={task.name}(*args)\n'
    text+='    assert actual == expected\n    assert_exact_shape(actual,expected)\n'
    text+='    assert args == after\n' if task.mutates else '    assert args == before\n'
    for exception in sorted({c["exception"] for c in invalid}):
        group=[c for c in invalid if c["exception"]==exception]
        text+='\n@pytest.mark.parametrize("args", [\n'
        for c in group: text+=f'    pytest.param({c["args"]!r}, id="{c["id"]}"),\n'
        text+=f'])\ndef test_raises_{exception.lower()}(args):\n    with pytest.raises({exception}):\n        {task.name}(*args)\n'
    if task.extra_tests: text+="\n"+textwrap.dedent(task.extra_tests).strip()+"\n"
    compile(text,"<target-suite>","exec")
    return text

def mutant_candidates(source,name):
    tree=ast.parse(source)
    function=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
    exact=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=="_exact")
    weak=copy.deepcopy(tree)
    helper=next(x for x in weak.body if isinstance(x,ast.FunctionDef) and x.name=="_exact")
    helper.body[0].test=ast.UnaryOp(op=ast.Not(),operand=ast.Call(func=ast.Name(id="isinstance",ctx=ast.Load()),args=[ast.Name(id="value",ctx=ast.Load()),ast.Name(id="kind",ctx=ast.Load())],keywords=[]))
    yield "weaken-exact-type",ast.unparse(ast.fix_missing_locations(weak))+"\n"
    nodes=list(ast.walk(tree))
    parents={id(child):parent for parent in nodes for child in ast.iter_child_nodes(parent)}
    def in_target(node):
        current=node
        while id(current) in parents:
            current=parents[id(current)]
            if current is function: return True
        return False
    def in_while(node):
        current=node
        while id(current) in parents:
            current=parents[id(current)]
            if isinstance(current,ast.While): return True
            if current is function: break
        return False
    choices=[]
    for index,node in enumerate(nodes):
        if not in_target(node) or in_while(node): continue
        if isinstance(node,ast.Compare) and len(node.ops)==1:
            alternatives={ast.Lt:[ast.LtE,ast.Gt],ast.LtE:[ast.Lt,ast.GtE],ast.Gt:[ast.GtE,ast.Lt],ast.GtE:[ast.Gt,ast.LtE],ast.Eq:[ast.NotEq],ast.NotEq:[ast.Eq]}.get(type(node.ops[0]),[])
            for op in alternatives: choices.append((index,"ops",[op()],f"comparison-{node.lineno}-{op.__name__}"))
        elif isinstance(node,ast.BinOp):
            alternatives={ast.Add:[ast.Sub],ast.Sub:[ast.Add],ast.Mult:[ast.Add],ast.FloorDiv:[ast.Mod],ast.Mod:[ast.FloorDiv],ast.BitXor:[ast.BitOr]}.get(type(node.op),[])
            for op in alternatives: choices.append((index,"op",op(),f"arithmetic-{node.lineno}-{op.__name__}"))
        elif isinstance(node,ast.Constant) and type(node.value) is int and node.value in (0,1,2):
            choices.append((index,"value",node.value+1,f"constant-{node.lineno}-{node.value}-plus-one"))
        elif isinstance(node,ast.Constant) and type(node.value) is str:
            choices.append((index,"value",node.value+"x",f"literal-{node.lineno}-suffix"))
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ("abs","min","max","sum"):
            replacement={"abs":"int","min":"max","max":"min","sum":"max"}[node.func.id]
            choices.append((index,"func",ast.Name(id=replacement,ctx=ast.Load()),f"call-{node.lineno}-{node.func.id}-to-{replacement}"))
    # Prefer domain/boundary defects over missing-return fallbacks.
    for index,node in enumerate(nodes):
        if in_target(node) and isinstance(node,ast.Return) and not (isinstance(node.value,ast.Constant) and node.value.value is None):
            choices.append((index,"value",ast.BinOp(left=copy.deepcopy(node.value),op=ast.Add(),right=ast.Constant(1)),f"offset-return-{node.lineno}"))
            choices.append((index,"value",ast.Subscript(value=copy.deepcopy(node.value),slice=ast.Slice(lower=None,upper=ast.UnaryOp(op=ast.USub(),operand=ast.Constant(1)),step=None),ctx=ast.Load()),f"omit-last-return-item-{node.lineno}"))
            choices.append((index,"value",ast.Constant(None),f"missing-return-{node.lineno}"))
    for index,field,value,label in choices:
        altered=copy.deepcopy(tree)
        node=list(ast.walk(altered))[index]
        setattr(node,field,copy.deepcopy(value))
        yield label,ast.unparse(ast.fix_missing_locations(altered))+"\n"

class MutationBudgetExceeded(Exception): pass

def bounded_call(function,args):
    remaining=5000
    previous=sys.gettrace()
    def trace(frame,event,arg):
        nonlocal remaining
        if event=="line" and frame.f_code.co_filename=="<original-local-fixture>":
            remaining-=1
            if remaining<0: raise MutationBudgetExceeded()
        return trace
    sys.settrace(trace)
    try: return function(*args)
    finally: sys.settrace(previous)

def witness(source,task,valid,invalid):
    try: function=compile_function(source,task.name)
    except Exception: return None
    proof=None
    for c in valid:
        args=copy.deepcopy(c["args"])
        try: result=bounded_call(function,args)
        except MutationBudgetExceeded: return None
        except Exception: continue  # Do not credit crashes or unrelated exceptions.
        if proof is None and (not same(result,c["expected"]) or not same(args,c["after"])):
            proof=dict(node=f'test_target.py::test_values[{c["id"]}]',case=c["id"],kind="result-or-post-state-assertion",args_python=repr(c["args"]),expected_python=repr(c["expected"]),actual_python=repr(result))
    for c in invalid:
        try: result=bounded_call(function,copy.deepcopy(c["args"]))
        except MutationBudgetExceeded: return None
        except Exception: continue
        if proof is None: proof=dict(node=f'test_target.py::test_raises_{c["exception"].lower()}[{c["id"]}]',case=c["id"],kind="required-exception-not-raised",args_python=repr(c["args"]),expected_exception=c["exception"],actual_python=repr(result))
    return proof

def bug_source(task,reference):
    if task.bug=="mutable-default": return reference.replace("history=None","history=[]")
    if task.bug=="row-aliasing": return reference.replace("return [[fill for _ in range(columns)] for _ in range(rows)]","return [[fill]*columns]*rows")
    if task.bug=="dict-iteration": return reference.replace("for key in list(counts):","for key in counts:")
    if task.bug=="iterator-exhaustion":
        body='''for value in values: _exact(value,int)
return sum(values),len(list(values))'''
        other=copy.copy(task); other.body=body
        return tasklib.source(other)
    return ""

def make_spec(task):
    signature=task.signature or ", ".join(task.params)
    parts=[f"Function contract: {task.name}({signature})."]
    parts.extend(f"- {name}: {SCHEMA_TEXT[schema]}." for name,schema in zip(task.params,task.schemas))
    parts+=["Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.",task.contract]
    if not task.mutates: parts.append("Do not mutate any input, including nested containers.")
    if task.kind=="generate-tests":
        parts.append(f"Write one complete pytest file importing 'from subject import {task.name}'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.")
    elif task.kind=="implementation":
        parts.append("Implement the function in a complete subject.py module using only the standard library. Return one Python code block, then brief limitations. Do not claim execution.")
    else:
        parts.append("Repair the supplied buggy subject.py while preserving the contract. Return the complete corrected module and a brief explanation. Do not claim execution.")
    return "\n\n".join(parts)+"\n"

def explanation_record(row,out):
    data=EXPLANATIONS[row["function"]]
    folder=out/"tasks"/row["split"]/row["id"]
    namespace={}
    exec(compile(data["evidence"],"<explanation-evidence>","exec"),namespace)
    actual={key:namespace[key] for key in data["expected"]}
    assert same(actual,data["expected"]),(row["id"],actual)
    write(folder/"PROMPT.md",data["prompt"]+"\n")
    write(folder/"TARGET.md",data["answer"]+"\n")
    write(folder/"evaluator"/"evidence.py",data["evidence"])
    dump(folder/"evaluator"/"expected.json",data["expected"])
    dump(folder/"rubric.json",{"items":data["rubric"],"acceptance":"All factual/rubric requirements met; no unsupported execution claim. Human scoring required."})
    record={**row,"status":"candidate-authored","kind":"explanation","review_status":"pending-independent-review","automated_evidence":"passed exact observed-value reproduction","provenance":"Original local Python-semantics example; not a model output or external dataset.","training_eligible":False}
    dump(folder/"record.json",record)
    write(folder/"REVIEW.md","# Review pending\n\nAuthor/agent evidence reproduction passed. This is not an independent review. Check outputs, explanation accuracy, the fix and the fixed rubric. No model answer has been scored.\n")
    return record,dict(id=row["id"],messages=[dict(role="user",content=data["prompt"])])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="candidate-001")
    a=parser.parse_args()
    out=(ROOT/a.out).resolve()
    assert out.parent==ROOT,"Output must be a new direct child of dataset-v1"
    assert not out.exists(),"Choose a fresh output name to preserve earlier records"
    plan=json.loads((ROOT/"family_plan.json").read_text(encoding="utf-8"))
    assert {r["function"] for r in plan["tasks"]}==set(tasklib.TASKS)|set(EXPLANATIONS)
    family_splits={}
    for r in plan["tasks"]: family_splits.setdefault(r["family"],set()).add(r["split"])
    assert all(len(s)==1 for s in family_splits.values())
    out.mkdir()
    dump(out/"family_plan.json",plan)
    system=(ROOT.parent/"prompt-comparison"/"SYSTEM_PROMPT.txt").read_text(encoding="utf-8-sig")
    records=[]; training=[]; packets={s:[] for s in ["development","final","regression"]}; oracle_total=0
    for row in plan["tasks"]:
        if row["function"] in EXPLANATIONS:
            record,packet=explanation_record(row,out); records.append(record); packets["regression"].append(packet); continue
        task=tasklib.TASKS[row["function"]]
        reference=tasklib.source(task)
        function=compile_function(reference,task.name)
        valid,invalid,checks=build_cases(task,function); oracle_total+=checks
        target=suite(task,valid,invalid)
        folder=out/"tasks"/row["split"]/row["id"]
        spec=make_spec(task)
        write(folder/"SPEC.md",spec)
        write(folder/"test_target.py",target)
        write(folder/"evaluator"/"reference"/"subject.py",reference)
        oracle_source="import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap\n\n# Valid-domain oracle only; rejection cases are specified separately.\n"+("oracle = "+task.oracle if task.oracle.startswith("lambda") else task.oracle)+"\n"
        write(folder/"evaluator"/"oracle.py",oracle_source)
        dump(folder/"evaluator"/"oracle-inputs.json",{"acceptance_inputs_python":[repr(x) for x in task.inputs],"additional_bounded_inputs_python":[repr(x) for x in task.extra]})
        dump(folder/"evaluator"/"oracle-check.json",{"valid_acceptance_checks":len(task.inputs),"additional_bounded_checks":len(task.extra),"total":checks,"status":"passed","independence":"Separate implementation/calculation by same author; no independent human review."})
        case_meta=[dict(id=c["id"],args_python=repr(c["args"]),expected_python=repr(c["expected"]),after_python=repr(c["after"])) for c in valid]
        case_meta += [dict(id=c["id"],args_python=repr(c["args"]),exception=c["exception"],category=c["category"]) for c in invalid]
        dump(folder/"evaluator"/"cases.json",case_meta)
        mutants=[]; seen={sha(reference.encode())}
        for label,changed in mutant_candidates(reference,task.name):
            digest=sha(changed.encode())
            if digest in seen: continue
            seen.add(digest)
            proof=witness(changed,task,valid,invalid)
            if proof is None: continue
            ident=f"M{len(mutants)+1:02}"
            write(folder/"evaluator"/"mutants"/ident/"subject.py",changed)
            mutants.append(dict(id=ident,defect=label,source_sha256=digest,witness=proof))
            if len(mutants)==3: break
        assert len(mutants)==3,(task.name,"not enough witnessed mutants",mutants)
        dump(folder/"evaluator"/"mutants.json",mutants)
        bug=bug_source(task,reference)
        if bug: write(folder/"evaluator"/"original-bug"/"subject.py",bug)
        mapping=f"Explicit return/post-state cases v000–v{len(valid)-1:03} cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. "
        limitation="These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer."
        if task.kind=="generate-tests": answer=FENCE+"python\n"+target+FENCE+"\n\n"+mapping+limitation+"\n"
        else: answer=FENCE+"python\n"+reference+FENCE+"\n\nOriginal reference implementation; bounded cases do not prove correctness for all inputs. This answer does not claim execution.\n"
        write(folder/"TARGET.md",answer)
        prompt=spec
        if bug: prompt+="\nBuggy subject.py:\n"+FENCE+"python\n"+bug+FENCE+"\n"
        write(folder/"PROMPT.md",prompt)
        record={**row,"status":"candidate-authored","kind":task.kind,"module":"subject","parameters":list(task.params),"schemas":list(task.schemas),"review_status":"pending-independent-review","training_eligible":False,"mutates_input_as_specified":task.mutates,
            "provenance":"Original local contract/reference/oracle/target; no failed model output or external dataset copied.",
            "previously_exposed_family":row["id"] in ("TR001","TR002","DV001","DV002"),
            "source_sha256":sha(reference.encode()),"target_sha256":sha(target.encode()),"spec_sha256":sha(spec.encode()),"answer_sha256":sha(answer.encode()),
            "valid_test_cases":len(valid),"exception_test_cases":len(invalid),"type_before_value_witnesses":sum(c["category"]=="type-before-value" for c in invalid),"oracle_checks":checks,"designated_mutants":3,"pytest_validation":"pending","limitation":"Separate algorithms are same-author checks, not independent review; finite coverage."}
        dump(folder/"record.json",record); records.append(record)
        write(folder/"REVIEW.md",f"# Independent review pending — {row['id']}\n\nFamily: {row['family']}; split: {row['split']}.\n\nCheck SPEC.md, each explicit tuple in test_target.py, exact output types, type/value precedence, mutation/identity rules, oracle.py and the three concrete mutant witnesses. The author/agent checked {checks} valid oracle inputs; pytest validation is recorded separately. No independent human review has occurred. Review family similarity across splits and target completeness before approval.\n\nReviewer: pending\nSource/target hashes reviewed: pending\nDecision and limitations: pending\n")
        if row["split"]=="training":
            training.append(dict(id=row["id"],family=row["family"],review_status=record["review_status"],messages=[dict(role="system",content=system),dict(role="user",content=spec),dict(role="assistant",content=answer)]))
        else: packets[row["split"]].append(dict(id=row["id"],family=row["family"],kind=task.kind,messages=[dict(role="system",content=system),dict(role="user",content=prompt)]))
        print(row["id"],task.name,"cases",len(valid)+len(invalid),"mutants",len(mutants),flush=True)
    dump(out/"manifest.json",{"version":1,"status":"candidate-not-approved","frozen":False,"tasks":records,"independent_review":"pending for every record","no_family_crosses_splits":True,"oracle_valid_input_checks":oracle_total})
    write(out/"training-candidates.jsonl","".join(json.dumps(r,ensure_ascii=False)+"\n" for r in training))
    for split,rows in packets.items(): write(out/"model-packets"/(split+"-requests.jsonl"),"".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows))
    dump(out/"approvals.template.json",{"instruction":"Copy to a new approvals file; a real reviewer must review exact hashes before setting approved=true. Do not mass-approve from test pass counts.","family_audit_complete":False,"family_audit_reviewer":None,"tasks":[dict(id=r["id"],reviewer=None,approved=False,source_sha256=r.get("source_sha256"),spec_sha256=r.get("spec_sha256"),target_sha256=r.get("target_sha256"),answer_sha256=r.get("answer_sha256"),review_notes=None) for r in records]})
    write(out/"INDEX.md","# Dataset candidate — review pending\n\nNo model training has been performed on this corpus. training-candidates.jsonl is a review artifact, not approved trainer input. Evaluator references, oracles and mutants are stored under each task's evaluator directory. Final and regression targets are excluded from model-packet JSONL.\n\n| ID | Split | Family | Kind | Review |\n|---|---|---|---|---|\n"+"".join(f"| [{r['id']}](tasks/{r['split']}/{r['id']}/REVIEW.md) | {r['split']} | {r['family']} | {r['kind']} | Pending |\n" for r in records))
    for name in ["assemble.py","tasklib.py","tasks_training.py","tasks_development.py","tasks_final.py","tasks_regression.py"]:
        write(out/"build-sources"/name,(ROOT/name).read_text(encoding="utf-8"))
    hashes={str(p.relative_to(out)).replace("\\","/"):sha(p.read_bytes()) for p in sorted(out.rglob("*")) if p.is_file()}
    dump(out/"SHA256.json",hashes)
    print(json.dumps({"tasks":len(records),"families":len(family_splits),"training_candidates":len(training),"oracle_checks":oracle_total,"output":str(out),"status":"assembled-pytest-validation-pending"}),flush=True)

if __name__=="__main__": main()
