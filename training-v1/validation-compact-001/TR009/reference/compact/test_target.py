import copy
import pytest
from subject import signed_gcd
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
    pytest.param((0, 8), 8),
    pytest.param((8, 0), 8),
    pytest.param((18, 12), 6),
    pytest.param((-18, 12), 6),
    pytest.param((18, -12), 6),
    pytest.param((-18, -12), 6),
    pytest.param((7, 13), 1),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=signed_gcd(*args)
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
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        signed_gcd(*args)
