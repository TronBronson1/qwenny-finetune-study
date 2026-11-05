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
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param(((), 0), (), id="v000"),
    pytest.param(((), 4), (), id="v001"),
    pytest.param(((1,), -9), (1,), id="v002"),
    pytest.param(((1, 2, 3), 0), (1, 2, 3), id="v003"),
    pytest.param(((1, 2, 3), 1), (3, 1, 2), id="v004"),
    pytest.param(((1, 2, 3), -1), (2, 3, 1), id="v005"),
    pytest.param(((1, 2, 3), 7), (3, 1, 2), id="v006"),
    pytest.param(((1, 1, 2), 2), (1, 2, 1), id="v007"),
    pytest.param((([1], {'k': 2}), 1), ({'k': 2}, [1]), id="v008"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=rotate_right(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((TupleChild(()), 0), id="e000"),
    pytest.param(([], 0), id="e001"),
    pytest.param((None, 0), id="e002"),
    pytest.param(((), True), id="e003"),
    pytest.param(((), IntChild(0)), id="e004"),
    pytest.param(((), 1.5), id="e005"),
    pytest.param(((), 'bad'), id="e006"),
    pytest.param(((), None), id="e007"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        rotate_right(*args)

def test_identity_and_no_element_mutation():
    first=[1]
    second={"k":2}
    third=object()
    values=(first,second,third)
    result=rotate_right(values,1)
    assert type(result) is tuple
    assert result[0] is third
    assert result[1] is first
    assert result[2] is second
    assert first == [1]
    assert second == {"k":2}
```

Explicit return/post-state cases v000–v008 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
