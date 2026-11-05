import pytest
from subject import parse_bool_word

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('true',), True, id="v000"),
    pytest.param(('false',), False, id="v001"),
])
def test_values(args,expected):
    actual=parse_bool_word(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('true'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('True'),), id="e008"),
    pytest.param((StrChild('false '),), id="e009"),
    pytest.param((StrChild(''),), id="e010"),
    pytest.param((StrChild('1'),), id="e011"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_bool_word(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('True',), id="e004"),
    pytest.param(('false ',), id="e005"),
    pytest.param(('',), id="e006"),
    pytest.param(('1',), id="e007"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_bool_word(*args)
