```python
import copy
import pytest
from subject import grid_neighbors

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
    pytest.param((0, 0, 1, 1), [], id="v000"),
    pytest.param((0, 0, 2, 3), [(0, 1), (1, 0)], id="v001"),
    pytest.param((1, 1, 3, 3), [(0, 1), (1, 2), (2, 1), (1, 0)], id="v002"),
    pytest.param((2, 2, 3, 3), [(1, 2), (2, 1)], id="v003"),
    pytest.param((0, 1, 1, 3), [(0, 2), (0, 0)], id="v004"),
    pytest.param((1, 0, 3, 1), [(0, 0), (2, 0)], id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=grid_neighbors(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 2, 2), id="e021"),
    pytest.param((2, 0, 2, 2), id="e022"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 1, 1), id="e000"),
    pytest.param((IntChild(0), 0, 1, 1), id="e001"),
    pytest.param((1.5, 0, 1, 1), id="e002"),
    pytest.param(('bad', 0, 1, 1), id="e003"),
    pytest.param((None, 0, 1, 1), id="e004"),
    pytest.param((0, True, 1, 1), id="e005"),
    pytest.param((0, IntChild(0), 1, 1), id="e006"),
    pytest.param((0, 1.5, 1, 1), id="e007"),
    pytest.param((0, 'bad', 1, 1), id="e008"),
    pytest.param((0, None, 1, 1), id="e009"),
    pytest.param((0, 0, True, 1), id="e010"),
    pytest.param((0, 0, IntChild(1), 1), id="e011"),
    pytest.param((0, 0, 1.5, 1), id="e012"),
    pytest.param((0, 0, 'bad', 1), id="e013"),
    pytest.param((0, 0, None, 1), id="e014"),
    pytest.param((0, 0, 1, True), id="e015"),
    pytest.param((0, 0, 1, IntChild(1)), id="e016"),
    pytest.param((0, 0, 1, 1.5), id="e017"),
    pytest.param((0, 0, 1, 'bad'), id="e018"),
    pytest.param((0, 0, 1, None), id="e019"),
    pytest.param((True, 0, 0, 1), id="e023"),
    pytest.param((-1, True, 2, 2), id="e024"),
    pytest.param((2, True, 2, 2), id="e025"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 0, 1), id="e020"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        grid_neighbors(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
