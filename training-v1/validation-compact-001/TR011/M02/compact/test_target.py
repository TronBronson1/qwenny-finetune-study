import copy
import pytest
from subject import leap_year
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
    pytest.param((1,), False),
    pytest.param((4,), True),
    pytest.param((1900,), False),
    pytest.param((2000,), True),
    pytest.param((2023,), False),
    pytest.param((2024,), True),
    pytest.param((2100,), False),
    pytest.param((9999,), False),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=leap_year(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True,)),
    pytest.param((IntChild(1),)),
    pytest.param((1.5,)),
    pytest.param(('bad',)),
    pytest.param((None,)),
    pytest.param((IntChild(0),)),
    pytest.param((IntChild(10000),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        leap_year(*args)
@pytest.mark.parametrize("args", [
    pytest.param((0,)),
    pytest.param((10000,)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        leap_year(*args)
