import copy
import pytest
from subject import format_cents
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
    pytest.param((0,), '0.00'),
    pytest.param((1,), '0.01'),
    pytest.param((-1,), '-0.01'),
    pytest.param((99,), '0.99'),
    pytest.param((100,), '1.00'),
    pytest.param((-100,), '-1.00'),
    pytest.param((12345,), '123.45'),
    pytest.param((1000000000000000000000000000001,), '10000000000000000000000000000.01'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=format_cents(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True,)),
    pytest.param((IntChild(0),)),
    pytest.param((1.5,)),
    pytest.param(('bad',)),
    pytest.param((None,)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        format_cents(*args)
