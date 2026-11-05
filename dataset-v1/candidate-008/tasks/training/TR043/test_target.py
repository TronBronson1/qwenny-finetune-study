import pytest
from subject import parse_binary

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('0',), 0, id="v000"),
    pytest.param(('1',), 1, id="v001"),
    pytest.param(('001',), 1, id="v002"),
    pytest.param(('1010',), 10, id="v003"),
    pytest.param(('11111111111111111111111111111111',), 4294967295, id="v004"),
])
def test_values(args,expected):
    actual=parse_binary(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild(''),), id="e010"),
    pytest.param((StrChild('2'),), id="e011"),
    pytest.param((StrChild(' 1'),), id="e012"),
    pytest.param((StrChild('111111111111111111111111111111111'),), id="e013"),
    pytest.param((StrChild('١٠'),), id="e014"),
    pytest.param((StrChild('１０'),), id="e015"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_binary(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('2',), id="e005"),
    pytest.param((' 1',), id="e006"),
    pytest.param(('111111111111111111111111111111111',), id="e007"),
    pytest.param(('١٠',), id="e008"),
    pytest.param(('１０',), id="e009"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_binary(*args)
