"""Verify concrete behavior differences on the eight already replayed copies."""
import copy,json,pathlib,runpy
EXP=pathlib.Path(__file__).resolve().parents[3]
WORK=pathlib.Path(__file__).resolve().parent
class IntChild(int): pass
CASES=[
("training","TR038",("٣f",),"ValueError",63),
("training","TR043",("١٠",),"ValueError",2),
("training","TR044",("[١:٣]",),"ValueError",(1,3)),
("training","TR056",("#١٢٣٤٥٦",),"ValueError",(18,52,86)),
("development","DV010",(["٣"],),"ValueError",3),
("development","DV008",("A","a"),None,0),
("development","DV011",([(IntChild(1),2)],),"TypeError",[(1,2)]),
("training","TR027",(["x"],),"TypeError",[])]
def call(fn,args):
    try: return dict(kind="return",value=repr(fn(*copy.deepcopy(args))))
    except Exception as error: return dict(kind="exception",exception=type(error).__name__,message=str(error))
results=[]
for split,task,args,exception,expected_mutant in CASES:
    record=json.loads((EXP/"dataset-v1/candidate-006/tasks"/split/task/"record.json").read_text(encoding="utf-8"))
    folder=WORK/"rubric_mutants"/(split+"_"+task)
    reference=runpy.run_path(str(folder/"reference/subject.py"))[record["function"]]
    mutant=runpy.run_path(str(folder/"rubric_mutant/subject.py"))[record["function"]]
    before=call(reference,args); after=call(mutant,args)
    if exception: assert before["kind"]=="exception" and before["exception"]==exception
    else: assert before==dict(kind="return",value="1")
    assert after==dict(kind="return",value=repr(expected_mutant))
    assert before!=after
    results.append(dict(task=task,split=split,function=record["function"],args_repr=repr(args),special_type="IntChild endpoints" if task=="DV011" else None,reference=before,mutant=after,behavioral_difference_confirmed=True))
(WORK/"behavior-witnesses.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(results,indent=2,ensure_ascii=False))

