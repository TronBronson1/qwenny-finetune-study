import copy
import pytest
from subject import roman_encode

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
    pytest.param((1,), 'I', (1,), id="v000"),
    pytest.param((4,), 'IV', (4,), id="v001"),
    pytest.param((9,), 'IX', (9,), id="v002"),
    pytest.param((40,), 'XL', (40,), id="v003"),
    pytest.param((90,), 'XC', (90,), id="v004"),
    pytest.param((400,), 'CD', (400,), id="v005"),
    pytest.param((900,), 'CM', (900,), id="v006"),
    pytest.param((1994,), 'MCMXCIV', (1994,), id="v007"),
    pytest.param((3999,), 'MMMCMXCIX', (3999,), id="v008"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=roman_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(1),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        roman_encode(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0,), id="e005"),
    pytest.param((4000,), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        roman_encode(*args)
