import pytest
from subject import parse_key_value

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('a=b',), ('a', 'b'), id="v000"),
    pytest.param(('a=',), ('a', ''), id="v001"),
    pytest.param(('a=b=c',), ('a', 'b=c'), id="v002"),
    pytest.param((' a = b ',), (' a ', ' b '), id="v003"),
    pytest.param(('é=字',), ('é', '字'), id="v004"),
])
def test_values(args,expected):
    actual=parse_key_value(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('a=b'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('a'),), id="e007"),
    pytest.param((StrChild('=a'),), id="e008"),
    pytest.param((StrChild(''),), id="e009"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_key_value(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('a',), id="e004"),
    pytest.param(('=a',), id="e005"),
    pytest.param(('',), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_key_value(*args)
