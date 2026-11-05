```python
import copy
import pytest
from subject import int_to_base

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
    pytest.param((0, 2), '0', id="v000"),
    pytest.param((1, 16), '1', id="v001"),
    pytest.param((15, 16), 'f', id="v002"),
    pytest.param((16, 16), '10', id="v003"),
    pytest.param((31, 2), '11111', id="v004"),
    pytest.param((81, 3), '10000', id="v005"),
    pytest.param((255, 16), 'ff', id="v006"),
    pytest.param((64, 8), '100', id="v007"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=int_to_base(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True, 2), id="e000"),
    pytest.param((IntChild(0), 2), id="e001"),
    pytest.param((1.5, 2), id="e002"),
    pytest.param(('bad', 2), id="e003"),
    pytest.param((None, 2), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(2)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
    pytest.param((-1, True), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        int_to_base(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 2), id="e010"),
    pytest.param((2, 1), id="e011"),
    pytest.param((2, 17), id="e012"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        int_to_base(*args)
```

Explicit return/post-state cases v000–v007 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
