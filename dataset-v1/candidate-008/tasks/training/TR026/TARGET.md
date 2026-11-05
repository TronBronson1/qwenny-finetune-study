```python
import copy
import pytest
from subject import stable_unique

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param(([1],), [1], id="v001"),
    pytest.param(([2, 1, 2, 3, 1],), [2, 1, 3], id="v002"),
    pytest.param(([0, 0, -1, -1],), [0, -1], id="v003"),
    pytest.param(([3, 2, 1],), [3, 2, 1], id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=stable_unique(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([True],), id="e001"),
    pytest.param(([IntChild(1)],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((['x'],), id="e005"),
    pytest.param(([1.5],), id="e006"),
    pytest.param(([-1.5],), id="e007"),
    pytest.param(([None],), id="e008"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        stable_unique(*args)
```

Return cases: empty=v000; single=v001; stable-order=v002; zero-negative=v003; already-unique=v004. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008. Exact returned types are checked recursively where specified. Valid-input preservation is checked before/after calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
