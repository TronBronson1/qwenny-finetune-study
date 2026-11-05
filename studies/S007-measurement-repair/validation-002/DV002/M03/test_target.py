import pytest
from subject import minute_of_day

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('00:00',), 0, id="v000"),
    pytest.param(('00:01',), 1, id="v001"),
    pytest.param(('01:00',), 60, id="v002"),
    pytest.param(('12:34',), 754, id="v003"),
    pytest.param(('23:59',), 1439, id="v004"),
])
def test_values(args,expected):
    actual=minute_of_day(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('00:00'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('24:00'),), id="e014"),
    pytest.param((StrChild('23:60'),), id="e015"),
    pytest.param((StrChild('1:00'),), id="e016"),
    pytest.param((StrChild('00:0'),), id="e017"),
    pytest.param((StrChild('00-00'),), id="e018"),
    pytest.param((StrChild(' 00:00'),), id="e019"),
    pytest.param((StrChild('00:00\n'),), id="e020"),
    pytest.param((StrChild('٠٠:٠٠'),), id="e021"),
    pytest.param((StrChild('٠١:٠٢'),), id="e022"),
    pytest.param((StrChild('０１:０２'),), id="e023"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        minute_of_day(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('24:00',), id="e004"),
    pytest.param(('23:60',), id="e005"),
    pytest.param(('1:00',), id="e006"),
    pytest.param(('00:0',), id="e007"),
    pytest.param(('00-00',), id="e008"),
    pytest.param((' 00:00',), id="e009"),
    pytest.param(('00:00\n',), id="e010"),
    pytest.param(('٠٠:٠٠',), id="e011"),
    pytest.param(('٠١:٠٢',), id="e012"),
    pytest.param(('０１:０２',), id="e013"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        minute_of_day(*args)
