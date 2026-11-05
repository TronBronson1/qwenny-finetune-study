import pytest
from subject import parse_unsigned

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('0',), 0, id="v000"),
    pytest.param(('1',), 1, id="v001"),
    pytest.param(('10',), 10, id="v002"),
    pytest.param(('999999999999',), 999999999999, id="v003"),
])
def test_values(args,expected):
    actual=parse_unsigned(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild(''),), id="e014"),
    pytest.param((StrChild('00'),), id="e015"),
    pytest.param((StrChild('+1'),), id="e016"),
    pytest.param((StrChild(' 1'),), id="e017"),
    pytest.param((StrChild('١'),), id="e018"),
    pytest.param((StrChild('1\n'),), id="e019"),
    pytest.param((StrChild('1000000000000'),), id="e020"),
    pytest.param((StrChild('٣'),), id="e021"),
    pytest.param((StrChild('３'),), id="e022"),
    pytest.param((StrChild('1٠'),), id="e023"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_unsigned(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('00',), id="e005"),
    pytest.param(('+1',), id="e006"),
    pytest.param((' 1',), id="e007"),
    pytest.param(('١',), id="e008"),
    pytest.param(('1\n',), id="e009"),
    pytest.param(('1000000000000',), id="e010"),
    pytest.param(('٣',), id="e011"),
    pytest.param(('３',), id="e012"),
    pytest.param(('1٠',), id="e013"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_unsigned(*args)
