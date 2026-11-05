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
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])
@pytest.mark.parametrize("args,expected", [
    pytest.param(((0, 0, 0), (0, 0, 0)), 0),
    pytest.param(((1, 2, 3), (1, 2, 4)), -1),
    pytest.param(((1, 3, 0), (1, 2, 99)), 1),
    pytest.param(((2, 0, 0), (1, 99, 99)), 1),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=compare_versions(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((TupleChild((0, 0, 0)), (0, 0, 0))),
    pytest.param(((True, 0, 0), (0, 0, 0))),
    pytest.param(((IntChild(1), 0, 0), (0, 0, 0))),
    pytest.param(([0, 0, 0], (0, 0, 0))),
    pytest.param((None, (0, 0, 0))),
    pytest.param(((0, 0, 0), TupleChild((0, 0, 0)))),
    pytest.param(((0, 0, 0), (True, 0, 0))),
    pytest.param(((0, 0, 0), (IntChild(1), 0, 0))),
    pytest.param(((0, 0, 0), [0, 0, 0])),
    pytest.param(((0, 0, 0), None)),
    pytest.param((TupleChild((1, 2)), (1, 2, 3))),
    pytest.param(((1, 2), TupleChild((1, 2, 3)))),
    pytest.param((TupleChild((1, -1, 0)), (1, 0, 0))),
    pytest.param(((1, -1, 0), TupleChild((1, 0, 0)))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        compare_versions(*args)
@pytest.mark.parametrize("args", [
    pytest.param(((1, 2), (1, 2, 3))),
    pytest.param(((1, -1, 0), (1, 0, 0))),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        compare_versions(*args)
