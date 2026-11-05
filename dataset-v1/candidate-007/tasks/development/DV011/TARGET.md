```python
import copy
import pytest
from subject import interval_union

class IntChild(int): pass
class ListChild(list): pass
class TupleChild(tuple): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param(([(1, 3)],), [(1, 3)], id="v001"),
    pytest.param(([(3, 5), (1, 3)],), [(1, 5)], id="v002"),
    pytest.param(([(1, 5), (2, 3)],), [(1, 5)], id="v003"),
    pytest.param(([(1, 2), (4, 6)],), [(1, 2), (4, 6)], id="v004"),
    pytest.param(([(-3, 0), (-1, 2)],), [(-3, 2)], id="v005"),
    pytest.param(([(5, 7), (1, 3), (2, 6)],), [(1, 7)], id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=interval_union(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([TupleChild((0, 1))],), id="e001"),
    pytest.param(([(0, True)],), id="e002"),
    pytest.param(([(0, 'x')],), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param(([1],), id="e005"),
    pytest.param(([(True, 1)],), id="e006"),
    pytest.param(([(IntChild(0), 1)],), id="e007"),
    pytest.param(([(0, IntChild(1))],), id="e008"),
    pytest.param(([('x', 1)],), id="e009"),
    pytest.param(([(1.5, 2)],), id="e010"),
    pytest.param(([(0, 1.5)],), id="e011"),
    pytest.param((ListChild([(1, 1)]),), id="e015"),
    pytest.param((ListChild([(2, 1)]),), id="e016"),
    pytest.param((ListChild([(1, 2, 3)]),), id="e017"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        interval_union(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([(1, 1)],), id="e012"),
    pytest.param(([(2, 1)],), id="e013"),
    pytest.param(([(1, 2, 3)],), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        interval_union(*args)
```

Return cases: empty=v000; single=v001; unordered-touching=v002; nested=v003; disjoint=v004; negative-overlap=v005; transitive-unordered-union=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e015,e016,e017; ValueError=e012,e013,e014. Exact returned types are checked recursively where specified. Valid-input preservation is checked before/after calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
