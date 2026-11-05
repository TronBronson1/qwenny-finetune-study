import copy
import pytest
from subject import wrap_index
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
    pytest.param((0, 1), 0),
    pytest.param((3, 3), 0),
    pytest.param((-1, 3), 2),
    pytest.param((-4, 3), 2),
    pytest.param((8, 3), 2),
    pytest.param((100000000000000000000, 7), 2),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=wrap_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 1)),
    pytest.param((IntChild(0), 1)),
    pytest.param((1.5, 1)),
    pytest.param(('bad', 1)),
    pytest.param((None, 1)),
    pytest.param((0, True)),
    pytest.param((0, IntChild(1))),
    pytest.param((0, 1.5)),
    pytest.param((0, 'bad')),
    pytest.param((0, None)),
    pytest.param((IntChild(0), 0)),
    pytest.param((0, IntChild(0))),
    pytest.param((IntChild(0), -1)),
    pytest.param((0, IntChild(-1))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        wrap_index(*args)
@pytest.mark.parametrize("args", [
    pytest.param((0, 0)),
    pytest.param((0, -1)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        wrap_index(*args)
