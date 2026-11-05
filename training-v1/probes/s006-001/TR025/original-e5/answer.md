```python
import copy
import pytest
from subject import run_length_encode

class StrChild(str): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass
class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param(
        (*ListChild([StrChild("a"),StrChild("b")]),),
        ListChild([]),
        id="v00000"
    ),
    pytest.param(
        (*ListChild([StrChild("a"),StrChild("b"),StrChild("a")]),),
        ListChild((StrChild("a"),IntChild(1)),(StrChild("b"),IntChild(1)),(StrChild("a"),IntChild(1))),
        id="v00001"
    ),
    pytest.param(
        (*ListChild([StrChild("x")]*4),),
        ListChild((StrChild("x"),IntChild(4))),
        id="v00002"
    ),
    pytest.param(
        (*ListChild([StrChild("a")]),(*ListChild([StrChild("b")]),)),
        ListChild((StrChild("a"),IntChild(1)),ListChild((StrChild("b"),IntChild(1)))),
        id="v00003"
    ),
    pytest.param(
        (*ListChild([StrChild("z")]),(*ListChild([StrChild("y")]),(*ListChild([StrChild("x")]),(*ListChild([StrChild("w")]),(*ListChild([StrChild("v")]),(*ListChild([StrChild("u")]),(*ListChild([StrChild("t")]),(*ListChild([StrChild("s")]),(*ListChild([StrChild("r")]),(*ListChild([StrChild("q")]),(*ListChild([StrChild("p")]),(*ListChild([StrChild("o")]),(*ListChild([StrChild("n")]),(*ListChild([StrChild("m")]),(*ListChild([StrChild("l")]),(*ListChild([StrChild("k")]),(*ListChild([StrChild("j")]),(*ListChild([StrChild("i")]),(*ListChild([StrChild("h")]),(*ListChild([StrChild("g")]),(*ListChild([StrChild("f")]),(*ListChild([StrChild("e")]),(*ListChild([StrChild("d")]),(*ListChild([StrChild("c")]),(*ListChild([StrChild("b")]),(*ListChild([StrChild("a")]),]))]))]))]))]))]))]))]))]))]))]))]))]))]))]),
        ListChild((StrChild("z"),IntChild(1)),ListChild((StrChild("y"),IntChild(1)),ListChild((StrChild("x"),IntChild(1)),ListChild((StrChild("w"),IntChild(1)),ListChild((StrChild("v"),IntChild(1)),ListChild((StrChild("u"),IntChild(1)),ListChild((StrChild("t"),IntChild(1)),ListChild((StrChild("s"),IntChild(1)),ListChild((StrChild("r"),IntChild(1)),ListChild((StrChild("q"),IntChild(1)),ListChild((StrChild("p"),IntChild(1)),ListChild((StrChild("o"),IntChild(1)),ListChild((StrChild("n"),IntChild(1)),ListChild((StrChild("m"),IntChild(1)),ListChild((StrChild("l"),IntChild(1)),ListChild((StrChild("k"),IntChild(1)),ListChild((StrChild("j"),IntChild(1)),ListChild((StrChild("i"),IntChild(1)),ListChild((StrChild("h"),IntChild(1)),ListChild((StrChild("g"),IntChild(1)),ListChild((StrChild("f"),IntChild(1)),ListChild((StrChild("e"),IntChild(1)),ListChild((StrChild("d"),IntChild(1)),ListChild((StrChild("c"),IntChild(1)),ListChild((StrChild("b"),IntChild(1)),ListChild((StrChild("a"),IntChild(1))))))))))))))))))))))))))))))))))))))))))))
    ),
    pytest.param(
        (*ListChild([StrChild("a"),StrChild("a")]),),
        ListChild((StrChild("a"),IntChild(2))),
        id="v00005"
    ),
    pytest.param(
        (*ListChild([StrChild("a")]),(*ListChild([StrChild("a")]),),),
        ListChild((StrChild("a"),IntChild(1)),ListChild((StrChild("a"),IntChild(1)))),
        id="v00006"
    ),
])
def run00000(args,expected):
    before=copy.deepcopy(args)
    actual=run_length_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(
        (ListChild([1]),),
        id="e00000"
    ),
    pytest.param(
        (1,),
        id="e00001"
    ),
    pytest.param(
        (StrChild(""),),
        id="e00002"
    ),
    pytest.param(
        (TupleChild(),),
        id="e00003"
    ),
    pytest.param(
        (ListChild([None]),),
        id="e00004"
    ),
])
def run00000_except(args):
    with pytest.raises((TypeError,)):
        run_length_encode(*args)
```

Explicit return/post-state cases v00000–v00006 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.