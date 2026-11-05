import copy
import pytest
from subject import weekday_offset
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
    pytest.param((0, 0), 0),
    pytest.param((0, 1), 1),
    pytest.param((6, 1), 0),
    pytest.param((0, -1), 6),
    pytest.param((3, 14), 3),
    pytest.param((3, -14), 3),
    pytest.param((6, 8), 0),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=weekday_offset(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 0)),
    pytest.param((IntChild(0), 0)),
    pytest.param((1.5, 0)),
    pytest.param(('bad', 0)),
    pytest.param((None, 0)),
    pytest.param((0, True)),
    pytest.param((0, IntChild(0))),
    pytest.param((0, 1.5)),
    pytest.param((0, 'bad')),
    pytest.param((0, None)),
    pytest.param((IntChild(-1), 0)),
    pytest.param((-1, IntChild(0))),
    pytest.param((IntChild(7), 0)),
    pytest.param((7, IntChild(0))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        weekday_offset(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1, 0)),
    pytest.param((7, 0)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        weekday_offset(*args)
