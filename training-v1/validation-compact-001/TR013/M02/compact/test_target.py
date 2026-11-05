import copy
import pytest
from subject import int_to_base
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
    pytest.param((0, 2), '0'),
    pytest.param((1, 16), '1'),
    pytest.param((15, 16), 'f'),
    pytest.param((16, 16), '10'),
    pytest.param((31, 2), '11111'),
    pytest.param((81, 3), '10000'),
    pytest.param((255, 16), 'ff'),
    pytest.param((64, 8), '100'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=int_to_base(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 2)),
    pytest.param((IntChild(0), 2)),
    pytest.param((1.5, 2)),
    pytest.param(('bad', 2)),
    pytest.param((None, 2)),
    pytest.param((0, True)),
    pytest.param((0, IntChild(2))),
    pytest.param((0, 1.5)),
    pytest.param((0, 'bad')),
    pytest.param((0, None)),
    pytest.param((IntChild(-1), 2)),
    pytest.param((-1, IntChild(2))),
    pytest.param((IntChild(2), 1)),
    pytest.param((2, IntChild(1))),
    pytest.param((IntChild(2), 17)),
    pytest.param((2, IntChild(17))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        int_to_base(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1, 2)),
    pytest.param((2, 1)),
    pytest.param((2, 17)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        int_to_base(*args)
