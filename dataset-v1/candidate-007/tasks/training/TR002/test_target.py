import pytest
from subject import strip_prefix

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('abc', 'a'), 'bc', id="v000"),
    pytest.param(('abc', 'abc'), '', id="v001"),
    pytest.param(('abc', 'z'), 'abc', id="v002"),
    pytest.param(('', 'a'), '', id="v003"),
    pytest.param(('aaaa', 'a'), 'aaa', id="v004"),
    pytest.param(('Abc', 'a'), 'Abc', id="v005"),
    pytest.param(('ba', 'a'), 'ba', id="v006"),
    pytest.param((' ab', ' '), 'ab', id="v007"),
    pytest.param(('éclair', 'é'), 'clair', id="v008"),
    pytest.param(('abc', 'abcd'), 'abc', id="v009"),
])
def test_values(args,expected):
    actual=strip_prefix(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('abc'), 'a'), id="e000"),
    pytest.param((b'x', 'a'), id="e001"),
    pytest.param((1, 'a'), id="e002"),
    pytest.param((None, 'a'), id="e003"),
    pytest.param(('abc', StrChild('a')), id="e004"),
    pytest.param(('abc', b'x'), id="e005"),
    pytest.param(('abc', 1), id="e006"),
    pytest.param(('abc', None), id="e007"),
    pytest.param((StrChild('abc'), ''), id="e010"),
    pytest.param(('abc', StrChild('')), id="e011"),
    pytest.param((StrChild(''), ''), id="e012"),
    pytest.param(('', StrChild('')), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        strip_prefix(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('abc', ''), id="e008"),
    pytest.param(('', ''), id="e009"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        strip_prefix(*args)
