```python
import pytest
from subject import wrap_index

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 1), 0, id="v000"),
    pytest.param((3, 3), 0, id="v001"),
    pytest.param((-1, 3), 2, id="v002"),
    pytest.param((-4, 3), 2, id="v003"),
    pytest.param((8, 3), 2, id="v004"),
    pytest.param((100000000000000000000, 7), 2, id="v005"),
])
def test_values(args,expected):
    actual=wrap_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 1), id="e000"),
    pytest.param((IntChild(0), 1), id="e001"),
    pytest.param((1.5, 1), id="e002"),
    pytest.param(('bad', 1), id="e003"),
    pytest.param((None, 1), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(1)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
    pytest.param((IntChild(0), 0), id="e012"),
    pytest.param((0, IntChild(0)), id="e013"),
    pytest.param((IntChild(0), -1), id="e014"),
    pytest.param((0, IntChild(-1)), id="e015"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        wrap_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0), id="e010"),
    pytest.param((0, -1), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        wrap_index(*args)
```

Return cases: unit-length=v000; positive-wrap=v001; negative-one=v002; negative-period=v003; positive-period=v004; large=v005. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e012,e013,e014,e015; ValueError=e010,e011. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
