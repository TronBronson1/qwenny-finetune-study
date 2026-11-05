```python
import pytest
from subject import signed_gcd

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 0), 0, id="v000"),
    pytest.param((0, 8), 8, id="v001"),
    pytest.param((8, 0), 8, id="v002"),
    pytest.param((18, 12), 6, id="v003"),
    pytest.param((-18, 12), 6, id="v004"),
    pytest.param((18, -12), 6, id="v005"),
    pytest.param((-18, -12), 6, id="v006"),
    pytest.param((7, 13), 1, id="v007"),
])
def test_values(args,expected):
    actual=signed_gcd(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0), id="e000"),
    pytest.param((IntChild(0), 0), id="e001"),
    pytest.param((1.5, 0), id="e002"),
    pytest.param(('bad', 0), id="e003"),
    pytest.param((None, 0), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(0)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        signed_gcd(*args)
```

Return cases: both-zero=v000; left-zero=v001; right-zero=v002; ordinary=v003; negative-left=v004; negative-right=v005; both-negative=v006; coprime=v007. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
