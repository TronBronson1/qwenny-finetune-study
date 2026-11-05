import copy
import pytest
from subject import parse_binary
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
    pytest.param(('0',), 0),
    pytest.param(('1',), 1),
    pytest.param(('001',), 1),
    pytest.param(('1010',), 10),
    pytest.param(('11111111111111111111111111111111',), 4294967295),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_binary(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0'),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild(''),)),
    pytest.param((StrChild('2'),)),
    pytest.param((StrChild(' 1'),)),
    pytest.param((StrChild('111111111111111111111111111111111'),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_binary(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('',)),
    pytest.param(('2',)),
    pytest.param((' 1',)),
    pytest.param(('111111111111111111111111111111111',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_binary(*args)
