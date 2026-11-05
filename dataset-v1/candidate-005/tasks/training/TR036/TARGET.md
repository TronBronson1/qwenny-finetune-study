```python
import copy
import pytest
from subject import lower_median

class IntChild(int): pass
class ListChild(list): pass

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
    pytest.param(([1],), 1, id="v000"),
    pytest.param(([4, 1],), 1, id="v001"),
    pytest.param(([9, 1, 5],), 5, id="v002"),
    pytest.param(([9, 1, 5, 3],), 3, id="v003"),
    pytest.param(([-1, -1, 0],), -1, id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=lower_median(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([1]),), id="e000"),
    pytest.param(([True],), id="e001"),
    pytest.param(([IntChild(1)],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        lower_median(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([],), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        lower_median(*args)
```

Explicit return/post-state cases v000–v004 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
