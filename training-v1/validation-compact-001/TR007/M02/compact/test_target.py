import copy
import pytest
from subject import digit_sum
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
    pytest.param((0,), 0),
    pytest.param((7,), 7),
    pytest.param((10,), 1),
    pytest.param((101,), 2),
    pytest.param((999,), 27),
    pytest.param((1000000000000000000000000000007,), 8),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=digit_sum(*args)
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
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        digit_sum(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1,)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        digit_sum(*args)
