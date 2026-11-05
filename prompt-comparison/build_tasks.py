"""Freeze new development tasks and evaluator-only fixtures."""
import json
import subprocess
import sys
from build_materials import ROOT, SHARED, write

tasks = [
    dict(id='T01', family='sequence-rotation', module='rotation', function='rotate_right',
         spec='Write tests for `from rotation import rotate_right`. rotate_right(values, steps) accepts only an exact built-in tuple for values and an exact built-in int for steps; reject subclasses and booleans. Validate both types first. Return a tuple rotated right by steps; negative steps rotate left, and steps wrap modulo length. Empty values returns (). Elements may be any Python objects and must retain their identity and relative order. Do not mutate elements. Test empty, singleton, zero, positive, negative and oversized rotations, duplicate elements, nested mutable elements and identity preservation. Isolate invalid types in both arguments.',
         ref='''def rotate_right(values, steps):
    if type(values) is not tuple or type(steps) is not int:
        raise TypeError
    if not values:
        return ()
    k = steps % len(values)
    return values[-k:] + values[:-k] if k else values[:]
''',
         tests='''import pytest
from rotation import rotate_right
class TupleChild(tuple): pass
class IntChild(int): pass
@pytest.mark.parametrize("values,steps,expected", [((),3,()), ((1,),-9,(1,)), ((1,2,3),0,(1,2,3)), ((1,2,3),1,(3,1,2)), ((1,2,3),-1,(2,3,1)), ((1,2,3),7,(3,1,2)), ((1,1,2),1,(2,1,1))])
def test_returns(values,steps,expected):
    assert rotate_right(values,steps) == expected
    assert type(rotate_right(values,steps)) is tuple
@pytest.mark.parametrize("values,steps", [([],1), (None,1), (TupleChild((1,2)),1), ((1,2),True), ((1,2),False), ((1,2),IntChild(1)), ((1,2),1.5), ((1,2),"1"), ((1,2),None), ((),True)])
def test_types(values,steps):
    with pytest.raises(TypeError): rotate_right(values,steps)
def test_identity_and_mutation():
    a,b = [1], {"x":2}
    result = rotate_right((a,b),1)
    assert result[0] is b and result[1] is a
    assert a == [1] and b == {"x":2}
''',
         mutants=[('direction','values[-k:] + values[:-k]','values[k:] + values[:k]'), ('no_modulo','steps % len(values)','steps'), ('bool_subclass','type(steps) is not int','not isinstance(steps, int)'), ('tuple_subclass','type(values) is not tuple','not isinstance(values, tuple)'), ('empty_validation','if type(values)', 'if not values: return ()\n    if type(values)')]),
    dict(id='T02', family='strict-clock-parsing', module='clock_parser', function='minute_of_day',
         spec='Write tests for `from clock_parser import minute_of_day`. minute_of_day(text) accepts only an exact built-in str; other types including str subclasses raise TypeError. Accept exactly five ASCII characters HH:MM with two ASCII digits per field and a colon at position 2. Hours are 00 through 23, minutes 00 through 59. Return hour*60+minute as an exact built-in int. All malformed strings raise ValueError. No whitespace trimming, signs, Unicode digits or extra characters. Test midnight, end of day, interior times, hour/minute bounds, shape errors, whitespace, Unicode digits and invalid types.',
         ref='''def minute_of_day(text):
    if type(text) is not str: raise TypeError
    if len(text) != 5 or text[2] != ":" or any(c not in "0123456789" for c in text[:2]+text[3:]): raise ValueError
    h,m = int(text[:2]),int(text[3:])
    if h > 23 or m > 59: raise ValueError
    return h*60+m
''',
         tests='''import pytest
from clock_parser import minute_of_day
class StrChild(str): pass
@pytest.mark.parametrize("text,expected", [("00:00",0),("23:59",1439),("12:34",754),("01:00",60),("00:01",1)])
def test_returns(text,expected):
    result=minute_of_day(text)
    assert result == expected and type(result) is int
@pytest.mark.parametrize("text", ["24:00","23:60","99:00","00:99","1:02","01:2","01-02","01:020",""," 01:02","01:02 ","+1:02","01:-2","０１:０２","٠١:٠٢","aa:bb"])
def test_values(text):
    with pytest.raises(ValueError): minute_of_day(text)
@pytest.mark.parametrize("text", [True,False,1,1.5,None,b"01:02",StrChild("01:02")])
def test_types(text):
    with pytest.raises(TypeError): minute_of_day(text)
''',
         mutants=[('hour_boundary','h > 23','h > 24'), ('minute_boundary','m > 59','m > 60'), ('arithmetic','return h*60+m','return h+m'), ('subclass','type(text) is not str','not isinstance(text,str)'), ('unicode','any(c not in "0123456789" for c in text[:2]+text[3:])','not (text[:2]+text[3:]).isdigit()')])
]
summary={}
for task in tasks:
    folder=ROOT/'evaluation'/task['id']
    write(folder/'TASK.txt',task['spec']+'\n\n'+SHARED+'\n')
    write(folder/'metadata.json',json.dumps({k:task[k] for k in ('id','family','module','function')},indent=2))
    write(folder/'EVALUATOR_TESTS.py',task['tests'])
    summary[task['id']]={}
    for name,source in [('reference',task['ref'])]+[(name,task['ref'].replace(old,new)) for name,old,new in task['mutants']]:
        target=folder/'fixtures'/name
        write(target/(task['module']+'.py'),source)
        write(target/'test_checked.py',task['tests'])
        p=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_checked.py'],cwd=target,capture_output=True,text=True,timeout=30)
        write(target/'checked.log',p.stdout+p.stderr)
        assert p.returncode==(0 if name=='reference' else 1),(task['id'],name,p.stdout)
        summary[task['id']][name]=p.stdout.strip().splitlines()[-1]
    for arm in ('A','B'):
        content=(('Fixed demonstrations:\n'+(ROOT/'DEMONSTRATIONS.md').read_text(encoding='utf-8')+'\n\nNew task:\n') if arm=='B' else '')+(folder/'TASK.txt').read_text(encoding='utf-8')
        write(ROOT/'packets'/f'{task["id"]}-{arm}.txt',content)
write(ROOT/'EVALUATOR_CHECKS.json',json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
