import copy
import pytest
from subject import clamp
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
    pytest.param((-1, 0, 5), 0),
    pytest.param((0, 0, 5), 0),
    pytest.param((3, 0, 5), 3),
    pytest.param((5, 0, 5), 5),
    pytest.param((6, 0, 5), 5),
    pytest.param((4, 2, 2), 2),
    pytest.param((-5, -4, -2), -4),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=clamp(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 5)),
    pytest.param((IntChild(-1), 0, 5)),
    pytest.param((1.5, 0, 5)),
    pytest.param(('bad', 0, 5)),
    pytest.param((None, 0, 5)),
    pytest.param((-1, True, 5)),
    pytest.param((-1, IntChild(0), 5)),
    pytest.param((-1, 1.5, 5)),
    pytest.param((-1, 'bad', 5)),
    pytest.param((-1, None, 5)),
    pytest.param((-1, 0, True)),
    pytest.param((-1, 0, IntChild(5))),
    pytest.param((-1, 0, 1.5)),
    pytest.param((-1, 0, 'bad')),
    pytest.param((-1, 0, None)),
    pytest.param((IntChild(1), 3, 2)),
    pytest.param((1, IntChild(3), 2)),
    pytest.param((1, 3, IntChild(2))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        clamp(*args)
@pytest.mark.parametrize("args", [
    pytest.param((1, 3, 2)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        clamp(*args)
