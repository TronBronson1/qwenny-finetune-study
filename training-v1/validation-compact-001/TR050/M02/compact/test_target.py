import copy
import pytest
from subject import unravel_index
class IntChild(int): pass
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
    pytest.param((0, 1, 1), (0, 0)),
    pytest.param((0, 2, 3), (0, 0)),
    pytest.param((2, 2, 3), (0, 2)),
    pytest.param((3, 2, 3), (1, 0)),
    pytest.param((5, 2, 3), (1, 2)),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=unravel_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((-1, 2, 3)),
    pytest.param((6, 2, 3)),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        unravel_index(*args)
@pytest.mark.parametrize("args", [
    pytest.param((True, 1, 1)),
    pytest.param((IntChild(0), 1, 1)),
    pytest.param((1.5, 1, 1)),
    pytest.param(('bad', 1, 1)),
    pytest.param((None, 1, 1)),
    pytest.param((0, True, 1)),
    pytest.param((0, IntChild(1), 1)),
    pytest.param((0, 1.5, 1)),
    pytest.param((0, 'bad', 1)),
    pytest.param((0, None, 1)),
    pytest.param((0, 1, True)),
    pytest.param((0, 1, IntChild(1))),
    pytest.param((0, 1, 1.5)),
    pytest.param((0, 1, 'bad')),
    pytest.param((0, 1, None)),
    pytest.param((IntChild(0), 0, 2)),
    pytest.param((0, IntChild(0), 2)),
    pytest.param((0, 0, IntChild(2))),
    pytest.param((IntChild(-1), 2, 3)),
    pytest.param((-1, IntChild(2), 3)),
    pytest.param((-1, 2, IntChild(3))),
    pytest.param((IntChild(6), 2, 3)),
    pytest.param((6, IntChild(2), 3)),
    pytest.param((6, 2, IntChild(3))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        unravel_index(*args)
@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 2)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        unravel_index(*args)
