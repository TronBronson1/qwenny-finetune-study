import copy
import pytest
from subject import parse_int_pair
class StrChild(str): pass
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
    pytest.param(('0,0',), (0, 0)),
    pytest.param(('-0,1',), (0, 1)),
    pytest.param(('-2,3',), (-2, 3)),
    pytest.param(('999999999999,-1',), (999999999999, -1)),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_int_pair(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0,0'),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild('1'),)),
    pytest.param((StrChild('1,2,3'),)),
    pytest.param((StrChild('01,2'),)),
    pytest.param((StrChild('+1,2'),)),
    pytest.param((StrChild('1, 2'),)),
    pytest.param((StrChild('١,2'),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_int_pair(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('1',)),
    pytest.param(('1,2,3',)),
    pytest.param(('01,2',)),
    pytest.param(('+1,2',)),
    pytest.param(('1, 2',)),
    pytest.param(('١,2',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_int_pair(*args)
