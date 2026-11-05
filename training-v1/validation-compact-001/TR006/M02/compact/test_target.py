import copy
import pytest
from subject import factorial
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
    pytest.param((0,), 1),
    pytest.param((1,), 1),
    pytest.param((2,), 2),
    pytest.param((5,), 120),
    pytest.param((12,), 479001600),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=factorial(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True,)),
    pytest.param((IntChild(0),)),
    pytest.param((1.5,)),
    pytest.param(('bad',)),
    pytest.param((None,)),
    pytest.param((IntChild(-1),)),
    pytest.param((IntChild(13),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        factorial(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1,)),
    pytest.param((13,)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        factorial(*args)
