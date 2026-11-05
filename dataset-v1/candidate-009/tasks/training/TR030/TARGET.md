```python
import copy
import pytest
from subject import transpose

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param(([[]],), [], id="v001"),
    pytest.param(([[], []],), [], id="v002"),
    pytest.param(([[1, 2], [3, 4]],), [[1, 3], [2, 4]], id="v003"),
    pytest.param(([[1, 2, 3]],), [[1], [2], [3]], id="v004"),
    pytest.param(([[1], [2], [3]],), [[1, 2, 3]], id="v005"),
    pytest.param(([[2, 1], [0, 3]],), [[2, 0], [1, 3]], id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=transpose(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([ListChild([1])],), id="e001"),
    pytest.param(([[True]],), id="e002"),
    pytest.param(([[IntChild(1)]],), id="e003"),
    pytest.param((['x'],), id="e004"),
    pytest.param((None,), id="e005"),
    pytest.param(([['x']],), id="e006"),
    pytest.param(([[1.5]],), id="e007"),
    pytest.param(([[None]],), id="e008"),
    pytest.param(([1],), id="e009"),
    pytest.param(((),), id="e011"),
    pytest.param(([(1,)],), id="e012"),
    pytest.param(([[1], None, [1, 2]],), id="e013"),
    pytest.param((ListChild([[1], [2, 3]]),), id="e014"),
    pytest.param(([[1], [1, 2], None],), id="e015"),
    pytest.param(([[1], [1, 2], [True]],), id="e016"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        transpose(*args)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([[1], [2, 3]],), id="e010"),
])
def test_raises_valueerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(ValueError):
        transpose(*args)
    assert args == before
```

Return cases: empty=v000; one-zero-column=v001; several-zero-columns=v002; square=v003; one-row=v004; one-column=v005; unsorted-rows=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e011,e012,e013,e014,e015,e016; ValueError=e010. Exact returned types are checked recursively where specified. Input preservation is checked before/after every call, including expected-exception calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
