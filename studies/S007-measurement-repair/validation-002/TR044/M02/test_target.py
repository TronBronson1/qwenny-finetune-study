import pytest
from subject import parse_range

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('[0:0]',), (0, 0), id="v000"),
    pytest.param(('[0:99]',), (0, 99), id="v001"),
    pytest.param(('[3:7]',), (3, 7), id="v002"),
    pytest.param(('[99:99]',), (99, 99), id="v003"),
])
def test_values(args,expected):
    actual=parse_range(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('[0:0]'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('[7:3]'),), id="e011"),
    pytest.param((StrChild('0:1'),), id="e012"),
    pytest.param((StrChild('[00:1]'),), id="e013"),
    pytest.param((StrChild('[0:100]'),), id="e014"),
    pytest.param((StrChild('[0:1] '),), id="e015"),
    pytest.param((StrChild('[١:٣]'),), id="e016"),
    pytest.param((StrChild('[１:３]'),), id="e017"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_range(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('[7:3]',), id="e004"),
    pytest.param(('0:1',), id="e005"),
    pytest.param(('[00:1]',), id="e006"),
    pytest.param(('[0:100]',), id="e007"),
    pytest.param(('[0:1] ',), id="e008"),
    pytest.param(('[١:٣]',), id="e009"),
    pytest.param(('[１:３]',), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_range(*args)
