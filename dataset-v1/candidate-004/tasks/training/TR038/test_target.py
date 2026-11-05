import copy
import pytest
from subject import parse_hex_byte

class IntChild(int): pass
class StrChild(str): pass
class BytesChild(bytes): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected,after", [
    pytest.param(('00',), 0, ('00',), id="v000"),
    pytest.param(('09',), 9, ('09',), id="v001"),
    pytest.param(('0a',), 10, ('0a',), id="v002"),
    pytest.param(('Af',), 175, ('Af',), id="v003"),
    pytest.param(('FF',), 255, ('FF',), id="v004"),
    pytest.param(('80',), 128, ('80',), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=parse_hex_byte(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('00'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_hex_byte(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('f',), id="e005"),
    pytest.param(('000',), id="e006"),
    pytest.param(('g0',), id="e007"),
    pytest.param((' ff',), id="e008"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_hex_byte(*args)
