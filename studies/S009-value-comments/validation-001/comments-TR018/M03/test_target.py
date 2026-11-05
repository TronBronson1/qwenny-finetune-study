import pytest
from subject import is_palindrome

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), True, id="v000"),
    pytest.param(('a',), True, id="v001"),
    pytest.param(('aa',), True, id="v002"),
    pytest.param(('aba',), True, id="v003"),
    pytest.param(('abba',), True, id="v004"),
    pytest.param(('ab',), False, id="v005"),
    pytest.param(('Aa',), False, id="v006"),
    pytest.param(('a a',), True, id="v007"),
    pytest.param(('é字é',), True, id="v008"),
    pytest.param(('a a!',), False, id="v009"),
])
def test_values(args,expected):
    actual=is_palindrome(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        is_palindrome(*args)
