import pytest
from subject import parse_signed

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('0',), 0, id="v000"),
    pytest.param(('-0',), 0, id="v001"),
    pytest.param(('+0',), 0, id="v002"),
    pytest.param(('0012',), 12, id="v003"),
    pytest.param(('-12',), -12, id="v004"),
    pytest.param(('+999999999999',), 999999999999, id="v005"),
])
def test_values(args,expected):
    actual=parse_signed(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild(''),), id="e012"),
    pytest.param((StrChild('+'),), id="e013"),
    pytest.param((StrChild('--1'),), id="e014"),
    pytest.param((StrChild('1 '),), id="e015"),
    pytest.param((StrChild('١'),), id="e016"),
    pytest.param((StrChild('1111111111111'),), id="e017"),
    pytest.param((StrChild('+١'),), id="e018"),
    pytest.param((StrChild('-１'),), id="e019"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_signed(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('+',), id="e005"),
    pytest.param(('--1',), id="e006"),
    pytest.param(('1 ',), id="e007"),
    pytest.param(('١',), id="e008"),
    pytest.param(('1111111111111',), id="e009"),
    pytest.param(('+١',), id="e010"),
    pytest.param(('-１',), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_signed(*args)
