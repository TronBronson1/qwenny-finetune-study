```python
import copy
import pytest
from subject import chunk_list

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([], 2), [], id="v000"),
    pytest.param(([1], 2), [[1]], id="v001"),
    pytest.param(([1, 2, 3, 4], 2), [[1, 2], [3, 4]], id="v002"),
    pytest.param(([1, 2, 3], 2), [[1, 2], [3]], id="v003"),
    pytest.param(([1, 2], 1), [[1], [2]], id="v004"),
    pytest.param(([1, 2], 9), [[1, 2]], id="v005"),
    pytest.param(([4, 2], 2), [[4, 2]], id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=chunk_list(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 2), id="e000"),
    pytest.param(([True], 2), id="e001"),
    pytest.param(([IntChild(1)], 2), id="e002"),
    pytest.param(((), 2), id="e003"),
    pytest.param((None, 2), id="e004"),
    pytest.param((['x'], 2), id="e005"),
    pytest.param(([1.5], 2), id="e006"),
    pytest.param(([-1.5], 2), id="e007"),
    pytest.param(([None], 2), id="e008"),
    pytest.param(([], True), id="e009"),
    pytest.param(([], IntChild(2)), id="e010"),
    pytest.param(([], 1.5), id="e011"),
    pytest.param(([], 'bad'), id="e012"),
    pytest.param(([], None), id="e013"),
    pytest.param(([1], -1.5), id="e016"),
    pytest.param((ListChild([1]), 0), id="e017"),
    pytest.param(([1], IntChild(0)), id="e018"),
    pytest.param((ListChild([]), -1), id="e019"),
    pytest.param(([], IntChild(-1)), id="e020"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        chunk_list(*args)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([1], 0), id="e014"),
    pytest.param(([], -1), id="e015"),
])
def test_raises_valueerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(ValueError):
        chunk_list(*args)
    assert args == before
```

Return cases: empty=v000; partial-single=v001; full-chunks=v002; last-partial=v003; unit-width=v004; oversize-width=v005; unsorted-values=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e012,e013,e016,e017,e018,e019,e020; ValueError=e014,e015. Exact returned types are checked recursively where specified. Input preservation is checked before/after every call, including expected-exception calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
