```python
import copy
import pytest
from subject import rotate_right

class IntChild(int): pass
class TupleChild(tuple): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) in (str,int,float,bool) for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param((), ()), id="v001"),
    pytest.param(((1,), ), ((1,)), id="v002"),
    pytest.param((TupleChild((1,)),), None, raises=TypeError, id="v003"),
    pytest.param(((IntChild(-1),), ), (IntChild(-1),), id="v004"),
    pytest.param(((), 1), ()), id="v005"),
    pytest.param(((1, 2), 2), (1, 2)), id="v006"),
    pytest.param(((2, 1), 1), (2, 1)), id="v007"),
    pytest.param(((2,), -1), (2,), id="v008"),
    pytest.param(((3,), 0), (3,), id="v009"),
    pytest.param(((3,), -1), (3,), id="v010"),
    pytest.param(((3,), 1), (3,), id="v011"),
    pytest.param(((3,), 2), (3,), id="v012"),
    pytest.param(([], 1), (), id="v013"),
    pytest.param(((True,False), 1), ((False,True),), id="v014"),
    pytest.param((((1,2),3), 1), (((3,1,2),),), id="v015"),
    pytest.param(((100, "a"), 3), (("a", 100, "b"),), id="v016"),
])
def test_values(args,expected): assert exact returned value equals expected and no extra keys/values.

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 1), id="e001"),
    pytest.param((SetChild({1}), 1), id="e002"),
    pytest.param((FrozenDict({"a":1}), 1), id="e003"),
    pytest.param((BytesChild(b'x'), 1), id="e004"),
    pytest.param((DecimalValue('inf'), 1), id="e005"),
])
def test_raises_type_error(args): with pytest.raises(TypeError): rotate_right(*args).

class ListChild(list): pass
class SetChild(set): pass
class FrozenDict(frozenset): pass # simplified for explicit typing check
class BytesChild(bytes): pass
class DecimalValue(float): pass

@pytest.mark.parametrize("args", [
    pytest.param((None, 1), id="e010"),
])
def test_raises_value_error(args): with pytest.raises(ValueError): rotate_right(*args).
```

Explicit return/post-state cases v001–v016 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified-invalid values and any listed type-before-value witnesses. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.