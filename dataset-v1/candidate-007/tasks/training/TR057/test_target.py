import pytest
from subject import make_slug

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param((' --_ ',), '', id="v001"),
    pytest.param(('Hello World',), 'hello-world', id="v002"),
    pytest.param((' A__b--C ',), 'a-b-c', id="v003"),
    pytest.param(('X9',), 'x9', id="v004"),
])
def test_values(args,expected):
    actual=make_slug(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('a/b'),), id="e009"),
    pytest.param((StrChild('é'),), id="e010"),
    pytest.param((StrChild('a\tb'),), id="e011"),
    pytest.param((StrChild('٣'),), id="e012"),
    pytest.param((StrChild('Ａ'),), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        make_slug(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('a/b',), id="e004"),
    pytest.param(('é',), id="e005"),
    pytest.param(('a\tb',), id="e006"),
    pytest.param(('٣',), id="e007"),
    pytest.param(('Ａ',), id="e008"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        make_slug(*args)
