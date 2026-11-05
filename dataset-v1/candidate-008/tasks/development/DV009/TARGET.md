```python
import copy
import pytest
from subject import lower_bound

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([], 0), 0, id="v000"),
    pytest.param(([1], 0), 0, id="v001"),
    pytest.param(([1], 1), 0, id="v002"),
    pytest.param(([1], 2), 1, id="v003"),
    pytest.param(([1, 2, 2, 4], 2), 1, id="v004"),
    pytest.param(([1, 2, 2, 4], 3), 3, id="v005"),
    pytest.param(([-3, -1, 0], -4), 0, id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=lower_bound(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 0), id="e000"),
    pytest.param(([True], 0), id="e001"),
    pytest.param(([IntChild(1)], 0), id="e002"),
    pytest.param(((), 0), id="e003"),
    pytest.param((None, 0), id="e004"),
    pytest.param((['x'], 0), id="e005"),
    pytest.param(([1.5], 0), id="e006"),
    pytest.param(([-1.5], 0), id="e007"),
    pytest.param(([None], 0), id="e008"),
    pytest.param(([], True), id="e009"),
    pytest.param(([], IntChild(0)), id="e010"),
    pytest.param(([], 1.5), id="e011"),
    pytest.param(([], 'bad'), id="e012"),
    pytest.param(([], None), id="e013"),
    pytest.param((ListChild([2, 1]), 1), id="e015"),
    pytest.param(([2, 1], IntChild(1)), id="e016"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        lower_bound(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([2, 1], 1), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        lower_bound(*args)
```

Return cases: empty=v000; before=v001; equal=v002; after=v003; leftmost-duplicate=v004; gap=v005; negative=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e012,e013,e015,e016; ValueError=e014. Exact returned types are checked recursively where specified. Valid-input preservation is checked before/after calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
