```python
import pytest
from subject import clamp

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((-1, 0, 5), 0, id="v000"),
    pytest.param((0, 0, 5), 0, id="v001"),
    pytest.param((3, 0, 5), 3, id="v002"),
    pytest.param((5, 0, 5), 5, id="v003"),
    pytest.param((6, 0, 5), 5, id="v004"),
    pytest.param((4, 2, 2), 2, id="v005"),
    pytest.param((-5, -4, -2), -4, id="v006"),
])
def test_values(args,expected):
    actual=clamp(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 5), id="e000"),
    pytest.param((IntChild(-1), 0, 5), id="e001"),
    pytest.param((1.5, 0, 5), id="e002"),
    pytest.param(('bad', 0, 5), id="e003"),
    pytest.param((None, 0, 5), id="e004"),
    pytest.param((-1, True, 5), id="e005"),
    pytest.param((-1, IntChild(0), 5), id="e006"),
    pytest.param((-1, 1.5, 5), id="e007"),
    pytest.param((-1, 'bad', 5), id="e008"),
    pytest.param((-1, None, 5), id="e009"),
    pytest.param((-1, 0, True), id="e010"),
    pytest.param((-1, 0, IntChild(5)), id="e011"),
    pytest.param((-1, 0, 1.5), id="e012"),
    pytest.param((-1, 0, 'bad'), id="e013"),
    pytest.param((-1, 0, None), id="e014"),
    pytest.param((IntChild(1), 3, 2), id="e016"),
    pytest.param((1, IntChild(3), 2), id="e017"),
    pytest.param((1, 3, IntChild(2)), id="e018"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        clamp(*args)

@pytest.mark.parametrize("args", [
    pytest.param((1, 3, 2), id="e015"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        clamp(*args)
```

Return cases: below=v000; lower-bound=v001; inside=v002; upper-bound=v003; above=v004; equal-bounds=v005; negative-bounds=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e012,e013,e014,e016,e017,e018; ValueError=e015. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
