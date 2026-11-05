import pytest
from subject import grid_neighbors

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 0, 1, 1), [], id="v000"),
    pytest.param((0, 0, 2, 3), [(0, 1), (1, 0)], id="v001"),
    pytest.param((1, 1, 3, 3), [(0, 1), (1, 2), (2, 1), (1, 0)], id="v002"),
    pytest.param((2, 2, 3, 3), [(1, 2), (2, 1)], id="v003"),
    pytest.param((0, 1, 1, 3), [(0, 2), (0, 0)], id="v004"),
    pytest.param((1, 0, 3, 1), [(0, 0), (2, 0)], id="v005"),
])
def test_values(args,expected):
    actual=grid_neighbors(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 2, 2), id="e021"),
    pytest.param((2, 0, 2, 2), id="e022"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 1, 1), id="e000"),
    pytest.param((IntChild(0), 0, 1, 1), id="e001"),
    pytest.param((1.5, 0, 1, 1), id="e002"),
    pytest.param(('bad', 0, 1, 1), id="e003"),
    pytest.param((None, 0, 1, 1), id="e004"),
    pytest.param((0, True, 1, 1), id="e005"),
    pytest.param((0, IntChild(0), 1, 1), id="e006"),
    pytest.param((0, 1.5, 1, 1), id="e007"),
    pytest.param((0, 'bad', 1, 1), id="e008"),
    pytest.param((0, None, 1, 1), id="e009"),
    pytest.param((0, 0, True, 1), id="e010"),
    pytest.param((0, 0, IntChild(1), 1), id="e011"),
    pytest.param((0, 0, 1.5, 1), id="e012"),
    pytest.param((0, 0, 'bad', 1), id="e013"),
    pytest.param((0, 0, None, 1), id="e014"),
    pytest.param((0, 0, 1, True), id="e015"),
    pytest.param((0, 0, 1, IntChild(1)), id="e016"),
    pytest.param((0, 0, 1, 1.5), id="e017"),
    pytest.param((0, 0, 1, 'bad'), id="e018"),
    pytest.param((0, 0, 1, None), id="e019"),
    pytest.param((IntChild(0), 0, 0, 1), id="e026"),
    pytest.param((0, IntChild(0), 0, 1), id="e027"),
    pytest.param((0, 0, IntChild(0), 1), id="e028"),
    pytest.param((0, 0, 0, IntChild(1)), id="e029"),
    pytest.param((IntChild(-1), 0, 2, 2), id="e030"),
    pytest.param((-1, IntChild(0), 2, 2), id="e031"),
    pytest.param((-1, 0, IntChild(2), 2), id="e032"),
    pytest.param((-1, 0, 2, IntChild(2)), id="e033"),
    pytest.param((IntChild(2), 0, 2, 2), id="e034"),
    pytest.param((2, IntChild(0), 2, 2), id="e035"),
    pytest.param((2, 0, IntChild(2), 2), id="e036"),
    pytest.param((2, 0, 2, IntChild(2)), id="e037"),
    pytest.param((IntChild(0), 0, 1, 0), id="e038"),
    pytest.param((0, IntChild(0), 1, 0), id="e039"),
    pytest.param((0, 0, IntChild(1), 0), id="e040"),
    pytest.param((0, 0, 1, IntChild(0)), id="e041"),
    pytest.param((IntChild(0), 0, 1, -1), id="e042"),
    pytest.param((0, IntChild(0), 1, -1), id="e043"),
    pytest.param((0, 0, IntChild(1), -1), id="e044"),
    pytest.param((0, 0, 1, IntChild(-1)), id="e045"),
    pytest.param((IntChild(0), 1, 1, 0), id="e046"),
    pytest.param((0, IntChild(1), 1, 0), id="e047"),
    pytest.param((0, 1, IntChild(1), 0), id="e048"),
    pytest.param((0, 1, 1, IntChild(0)), id="e049"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 0, 1), id="e020"),
    pytest.param((0, 0, 1, 0), id="e023"),
    pytest.param((0, 0, 1, -1), id="e024"),
    pytest.param((0, 1, 1, 0), id="e025"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        grid_neighbors(*args)
