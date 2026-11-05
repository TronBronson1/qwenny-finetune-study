```python
import copy
import pytest
from subject import compare_versions

class IntChild(int): pass
class TupleChild(tuple): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(((0, 0, 0), (0, 0, 0)), 0, id="v000"),
    pytest.param(((1, 2, 3), (1, 2, 4)), -1, id="v001"),
    pytest.param(((1, 3, 0), (1, 2, 99)), 1, id="v002"),
    pytest.param(((2, 0, 0), (1, 99, 99)), 1, id="v003"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=compare_versions(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((TupleChild((0, 0, 0)), (0, 0, 0)), id="e000"),
    pytest.param(((True, 0, 0), (0, 0, 0)), id="e001"),
    pytest.param(((IntChild(1), 0, 0), (0, 0, 0)), id="e002"),
    pytest.param(([0, 0, 0], (0, 0, 0)), id="e003"),
    pytest.param((None, (0, 0, 0)), id="e004"),
    pytest.param((('x', 0, 0), (0, 0, 0)), id="e005"),
    pytest.param(((1.5, 0, 0), (0, 0, 0)), id="e006"),
    pytest.param(((None, 0, 0), (0, 0, 0)), id="e007"),
    pytest.param(((IntChild(0), 0, 0), (0, 0, 0)), id="e008"),
    pytest.param(((0, 'x', 0), (0, 0, 0)), id="e009"),
    pytest.param(((0, 1.5, 0), (0, 0, 0)), id="e010"),
    pytest.param(((0, None, 0), (0, 0, 0)), id="e011"),
    pytest.param(((0, True, 0), (0, 0, 0)), id="e012"),
    pytest.param(((0, IntChild(0), 0), (0, 0, 0)), id="e013"),
    pytest.param(((0, 0, 'x'), (0, 0, 0)), id="e014"),
    pytest.param(((0, 0, 1.5), (0, 0, 0)), id="e015"),
    pytest.param(((0, 0, None), (0, 0, 0)), id="e016"),
    pytest.param(((0, 0, True), (0, 0, 0)), id="e017"),
    pytest.param(((0, 0, IntChild(0)), (0, 0, 0)), id="e018"),
    pytest.param(((0, 0, 0), TupleChild((0, 0, 0))), id="e019"),
    pytest.param(((0, 0, 0), (True, 0, 0)), id="e020"),
    pytest.param(((0, 0, 0), (IntChild(1), 0, 0)), id="e021"),
    pytest.param(((0, 0, 0), [0, 0, 0]), id="e022"),
    pytest.param(((0, 0, 0), None), id="e023"),
    pytest.param(((0, 0, 0), ('x', 0, 0)), id="e024"),
    pytest.param(((0, 0, 0), (1.5, 0, 0)), id="e025"),
    pytest.param(((0, 0, 0), (None, 0, 0)), id="e026"),
    pytest.param(((0, 0, 0), (IntChild(0), 0, 0)), id="e027"),
    pytest.param(((0, 0, 0), (0, 'x', 0)), id="e028"),
    pytest.param(((0, 0, 0), (0, 1.5, 0)), id="e029"),
    pytest.param(((0, 0, 0), (0, None, 0)), id="e030"),
    pytest.param(((0, 0, 0), (0, True, 0)), id="e031"),
    pytest.param(((0, 0, 0), (0, IntChild(0), 0)), id="e032"),
    pytest.param(((0, 0, 0), (0, 0, 'x')), id="e033"),
    pytest.param(((0, 0, 0), (0, 0, 1.5)), id="e034"),
    pytest.param(((0, 0, 0), (0, 0, None)), id="e035"),
    pytest.param(((0, 0, 0), (0, 0, True)), id="e036"),
    pytest.param(((0, 0, 0), (0, 0, IntChild(0))), id="e037"),
    pytest.param((TupleChild((1, 2)), (1, 2, 3)), id="e046"),
    pytest.param(((1, 2), TupleChild((1, 2, 3))), id="e047"),
    pytest.param((TupleChild((1, -1, 0)), (1, 0, 0)), id="e048"),
    pytest.param(((1, -1, 0), TupleChild((1, 0, 0))), id="e049"),
    pytest.param((TupleChild((-1, 0, 0)), (0, 0, 0)), id="e050"),
    pytest.param(((-1, 0, 0), TupleChild((0, 0, 0))), id="e051"),
    pytest.param((TupleChild((0, -1, 0)), (0, 0, 0)), id="e052"),
    pytest.param(((0, -1, 0), TupleChild((0, 0, 0))), id="e053"),
    pytest.param((TupleChild((0, 0, -1)), (0, 0, 0)), id="e054"),
    pytest.param(((0, 0, -1), TupleChild((0, 0, 0))), id="e055"),
    pytest.param((TupleChild((0, 0, 0)), (-1, 0, 0)), id="e056"),
    pytest.param(((0, 0, 0), TupleChild((-1, 0, 0))), id="e057"),
    pytest.param((TupleChild((0, 0, 0)), (0, -1, 0)), id="e058"),
    pytest.param(((0, 0, 0), TupleChild((0, -1, 0))), id="e059"),
    pytest.param((TupleChild((0, 0, 0)), (0, 0, -1)), id="e060"),
    pytest.param(((0, 0, 0), TupleChild((0, 0, -1))), id="e061"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        compare_versions(*args)

@pytest.mark.parametrize("args", [
    pytest.param(((1, 2), (1, 2, 3)), id="e038"),
    pytest.param(((1, -1, 0), (1, 0, 0)), id="e039"),
    pytest.param(((-1, 0, 0), (0, 0, 0)), id="e040"),
    pytest.param(((0, -1, 0), (0, 0, 0)), id="e041"),
    pytest.param(((0, 0, -1), (0, 0, 0)), id="e042"),
    pytest.param(((0, 0, 0), (-1, 0, 0)), id="e043"),
    pytest.param(((0, 0, 0), (0, -1, 0)), id="e044"),
    pytest.param(((0, 0, 0), (0, 0, -1)), id="e045"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        compare_versions(*args)
```

Return cases: equal=v000; less=v001; greater-middle=v002; lexicographic-major=v003. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007,e008,e009,e010,e011,e012,e013,e014,e015,e016,e017,e018,e019,e020,e021,e022,e023,e024,e025,e026,e027,e028,e029,e030,e031,e032,e033,e034,e035,e036,e037,e046,e047,e048,e049,e050,e051,e052,e053,e054,e055,e056,e057,e058,e059,e060,e061; ValueError=e038,e039,e040,e041,e042,e043,e044,e045. Exact returned types are checked recursively where specified. Valid-input preservation is checked before/after calls. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
