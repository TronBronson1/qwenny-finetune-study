import pytest
from subject import keypad_encode

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param(('ABC',), '222', id="v001"),
    pytest.param(('HELLO',), '43556', id="v002"),
    pytest.param(('PQRS',), '7777', id="v003"),
    pytest.param(('WXYZ',), '9999', id="v004"),
    pytest.param(('ABCDEFGHIJKLMNOPQRSTUVWXYZ',), '22233344455566677778889999', id="v005"),
])
def test_values(args,expected):
    actual=keypad_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('abc'),), id="e008"),
    pytest.param((StrChild('A B'),), id="e009"),
    pytest.param((StrChild('É'),), id="e010"),
    pytest.param((StrChild('Ａ'),), id="e011"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        keypad_encode(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('abc',), id="e004"),
    pytest.param(('A B',), id="e005"),
    pytest.param(('É',), id="e006"),
    pytest.param(('Ａ',), id="e007"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        keypad_encode(*args)
