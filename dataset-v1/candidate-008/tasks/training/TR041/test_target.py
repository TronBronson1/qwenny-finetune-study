import pytest
from subject import parse_int_pair

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('0,0',), (0, 0), id="v000"),
    pytest.param(('-0,1',), (0, 1), id="v001"),
    pytest.param(('-2,3',), (-2, 3), id="v002"),
    pytest.param(('999999999999,-1',), (999999999999, -1), id="v003"),
    pytest.param(('-999999999999,999999999999',), (-999999999999, 999999999999), id="v004"),
])
def test_values(args,expected):
    actual=parse_int_pair(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0,0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('1'),), id="e015"),
    pytest.param((StrChild('1,2,3'),), id="e016"),
    pytest.param((StrChild('01,2'),), id="e017"),
    pytest.param((StrChild('+1,2'),), id="e018"),
    pytest.param((StrChild('1, 2'),), id="e019"),
    pytest.param((StrChild('١,2'),), id="e020"),
    pytest.param((StrChild('٣,4'),), id="e021"),
    pytest.param((StrChild('3,４'),), id="e022"),
    pytest.param((StrChild('0,1000000000000'),), id="e023"),
    pytest.param((StrChild('1٠,2'),), id="e024"),
    pytest.param((StrChild('1,2٠'),), id="e025"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_int_pair(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('1',), id="e004"),
    pytest.param(('1,2,3',), id="e005"),
    pytest.param(('01,2',), id="e006"),
    pytest.param(('+1,2',), id="e007"),
    pytest.param(('1, 2',), id="e008"),
    pytest.param(('١,2',), id="e009"),
    pytest.param(('٣,4',), id="e010"),
    pytest.param(('3,４',), id="e011"),
    pytest.param(('0,1000000000000',), id="e012"),
    pytest.param(('1٠,2',), id="e013"),
    pytest.param(('1,2٠',), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_int_pair(*args)
