import copy
import pytest
from subject import parse_hex_byte
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
    pytest.param(('00',), 0),
    pytest.param(('09',), 9),
    pytest.param(('0a',), 10),
    pytest.param(('Af',), 175),
    pytest.param(('FF',), 255),
    pytest.param(('80',), 128),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_hex_byte(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('00'),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild(''),)),
    pytest.param((StrChild('f'),)),
    pytest.param((StrChild('000'),)),
    pytest.param((StrChild('g0'),)),
    pytest.param((StrChild(' ff'),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_hex_byte(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('',)),
    pytest.param(('f',)),
    pytest.param(('000',)),
    pytest.param(('g0',)),
    pytest.param((' ff',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_hex_byte(*args)
