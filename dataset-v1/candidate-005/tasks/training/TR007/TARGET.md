```python
import copy
import pytest
from subject import digit_sum

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
    pytest.param((0,), 0, id="v000"),
    pytest.param((7,), 7, id="v001"),
    pytest.param((10,), 1, id="v002"),
    pytest.param((101,), 2, id="v003"),
    pytest.param((999,), 27, id="v004"),
    pytest.param((1000000000000000000000000000007,), 8, id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=digit_sum(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        digit_sum(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1,), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        digit_sum(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
