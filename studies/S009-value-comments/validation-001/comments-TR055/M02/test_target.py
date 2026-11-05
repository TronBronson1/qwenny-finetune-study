import pytest
from subject import encode_rgb

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 0, 0), '#000000', id="v000"),
    pytest.param((255, 255, 255), '#ffffff', id="v001"),
    pytest.param((1, 2, 3), '#010203', id="v002"),
    pytest.param((0, 128, 255), '#0080ff', id="v003"),
])
def test_values(args,expected):
    actual=encode_rgb(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 0), id="e000"),
    pytest.param((IntChild(0), 0, 0), id="e001"),
    pytest.param((1.5, 0, 0), id="e002"),
    pytest.param(('bad', 0, 0), id="e003"),
    pytest.param((None, 0, 0), id="e004"),
    pytest.param((0, True, 0), id="e005"),
    pytest.param((0, IntChild(0), 0), id="e006"),
    pytest.param((0, 1.5, 0), id="e007"),
    pytest.param((0, 'bad', 0), id="e008"),
    pytest.param((0, None, 0), id="e009"),
    pytest.param((0, 0, True), id="e010"),
    pytest.param((0, 0, IntChild(0)), id="e011"),
    pytest.param((0, 0, 1.5), id="e012"),
    pytest.param((0, 0, 'bad'), id="e013"),
    pytest.param((0, 0, None), id="e014"),
    pytest.param((IntChild(-1), 0, 0), id="e018"),
    pytest.param((-1, IntChild(0), 0), id="e019"),
    pytest.param((-1, 0, IntChild(0)), id="e020"),
    pytest.param((IntChild(0), 256, 0), id="e021"),
    pytest.param((0, IntChild(256), 0), id="e022"),
    pytest.param((0, 256, IntChild(0)), id="e023"),
    pytest.param((IntChild(0), 0, -1), id="e024"),
    pytest.param((0, IntChild(0), -1), id="e025"),
    pytest.param((0, 0, IntChild(-1)), id="e026"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        encode_rgb(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 0), id="e015"),
    pytest.param((0, 256, 0), id="e016"),
    pytest.param((0, 0, -1), id="e017"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        encode_rgb(*args)
