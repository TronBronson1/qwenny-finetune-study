import pytest
from subject import decode_rgb

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('#000000',), (0, 0, 0), id="v000"),
    pytest.param(('#ffffff',), (255, 255, 255), id="v001"),
    pytest.param(('#010203',), (1, 2, 3), id="v002"),
    pytest.param(('#00aAFF',), (0, 170, 255), id="v003"),
])
def test_values(args,expected):
    actual=decode_rgb(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('#000000'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('ffffff'),), id="e010"),
    pytest.param((StrChild('#fff'),), id="e011"),
    pytest.param((StrChild('#gg0000'),), id="e012"),
    pytest.param((StrChild('#000000\n'),), id="e013"),
    pytest.param((StrChild('#١٢٣٤٥٦'),), id="e014"),
    pytest.param((StrChild('#１２３４５６'),), id="e015"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        decode_rgb(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('ffffff',), id="e004"),
    pytest.param(('#fff',), id="e005"),
    pytest.param(('#gg0000',), id="e006"),
    pytest.param(('#000000\n',), id="e007"),
    pytest.param(('#١٢٣٤٥٦',), id="e008"),
    pytest.param(('#１２３４５６',), id="e009"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        decode_rgb(*args)
