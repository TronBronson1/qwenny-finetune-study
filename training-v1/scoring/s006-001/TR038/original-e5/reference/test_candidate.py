import copy
import pytest
from subject import parse_hex_byte

class StrChild(str):
    pass

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
    pytest.param( ('ab',), 0xAB, id="v000")
    ,pytest.param( ('AB',), 0xAB, id="v001")
    ,pytest.param( ('00',), 0, id="v002")
    ,pytest.param( ('7f',), 0x7F, id="v003")
    ,pytest.param( ('ff',), 0xFF, id="v004")
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_hex_byte(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param( (StrChild('x'),), id="e000")
    ,pytest.param( (b'x',), id="e001")
    ,pytest.param( (123,), id="e002")
    ,pytest.param( (None,), id="e003")
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_hex_byte(*args)

@pytest.mark.parametrize("args", [
    pytest.param( ('x',), id="e004")
    ,pytest.param( ('GG',), id="e005")
    ,pytest.param( ('1G',), id="e006")
    ,pytest.param( ('',), id="e007")
    ,pytest.param( ('012',), id="e008")
    ,pytest.param( (' 1',), id="e009")
    ,pytest.param( ('\n',), id="e010")
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_hex_byte(*args)
