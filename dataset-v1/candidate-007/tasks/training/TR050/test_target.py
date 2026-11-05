import pytest
from subject import unravel_index

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 1, 1), (0, 0), id="v000"),
    pytest.param((0, 2, 3), (0, 0), id="v001"),
    pytest.param((2, 2, 3), (0, 2), id="v002"),
    pytest.param((3, 2, 3), (1, 0), id="v003"),
    pytest.param((5, 2, 3), (1, 2), id="v004"),
])
def test_values(args,expected):
    actual=unravel_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 2, 3), id="e016"),
    pytest.param((6, 2, 3), id="e017"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        unravel_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((True, 1, 1), id="e000"),
    pytest.param((IntChild(0), 1, 1), id="e001"),
    pytest.param((1.5, 1, 1), id="e002"),
    pytest.param(('bad', 1, 1), id="e003"),
    pytest.param((None, 1, 1), id="e004"),
    pytest.param((0, True, 1), id="e005"),
    pytest.param((0, IntChild(1), 1), id="e006"),
    pytest.param((0, 1.5, 1), id="e007"),
    pytest.param((0, 'bad', 1), id="e008"),
    pytest.param((0, None, 1), id="e009"),
    pytest.param((0, 1, True), id="e010"),
    pytest.param((0, 1, IntChild(1)), id="e011"),
    pytest.param((0, 1, 1.5), id="e012"),
    pytest.param((0, 1, 'bad'), id="e013"),
    pytest.param((0, 1, None), id="e014"),
    pytest.param((IntChild(0), 0, 2), id="e018"),
    pytest.param((0, IntChild(0), 2), id="e019"),
    pytest.param((0, 0, IntChild(2)), id="e020"),
    pytest.param((IntChild(-1), 2, 3), id="e021"),
    pytest.param((-1, IntChild(2), 3), id="e022"),
    pytest.param((-1, 2, IntChild(3)), id="e023"),
    pytest.param((IntChild(6), 2, 3), id="e024"),
    pytest.param((6, IntChild(2), 3), id="e025"),
    pytest.param((6, 2, IntChild(3)), id="e026"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        unravel_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 2), id="e015"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        unravel_index(*args)
