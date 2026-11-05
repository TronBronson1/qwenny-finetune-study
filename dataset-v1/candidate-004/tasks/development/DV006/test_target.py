import copy
import pytest
from subject import keypad_encode

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
    pytest.param(('',), '', ('',), id="v000"),
    pytest.param(('ABC',), '222', ('ABC',), id="v001"),
    pytest.param(('HELLO',), '43556', ('HELLO',), id="v002"),
    pytest.param(('PQRS',), '7777', ('PQRS',), id="v003"),
    pytest.param(('WXYZ',), '9999', ('WXYZ',), id="v004"),
    pytest.param(('ABCDEFGHIJKLMNOPQRSTUVWXYZ',), '22233344455566677778889999', ('ABCDEFGHIJKLMNOPQRSTUVWXYZ',), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=keypad_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        keypad_encode(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('abc',), id="e004"),
    pytest.param(('A B',), id="e005"),
    pytest.param(('É',), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        keypad_encode(*args)
