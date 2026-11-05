```python
import pytest
from subject import grouped_decimal

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), '0', id="v000"),
    pytest.param((1,), '1', id="v001"),
    pytest.param((999,), '999', id="v002"),
    pytest.param((1000,), '1_000', id="v003"),
    pytest.param((-1000,), '-1_000', id="v004"),
    pytest.param((1234567,), '1_234_567', id="v005"),
    pytest.param((1000000000000000000000000000000,), '1_000_000_000_000_000_000_000_000_000_000', id="v006"),
])
def test_values(args,expected):
    actual=grouped_decimal(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        grouped_decimal(*args)
```

Return cases: zero=v000; single=v001; last-ungrouped=v002; first-grouped=v003; negative=v004; several-groups=v005; large=v006. Validation cases: TypeError=e000,e001,e002,e003,e004. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
