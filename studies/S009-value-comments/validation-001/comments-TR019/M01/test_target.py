import pytest
from subject import normalize_newlines

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param(('a',), 'a', id="v001"),
    pytest.param(('\r\n',), '\n', id="v002"),
    pytest.param(('\r',), '\n', id="v003"),
    pytest.param(('\n',), '\n', id="v004"),
    pytest.param(('a\r\nb\rc\nd',), 'a\nb\nc\nd', id="v005"),
    pytest.param(('\r\r\n',), '\n\n', id="v006"),
])
def test_values(args,expected):
    actual=normalize_newlines(*args)
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
        normalize_newlines(*args)
