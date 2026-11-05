import pytest
from subject import row_major_offset

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 0, 1, 1), 0, id="v000"),
    pytest.param((0, 2, 2, 3), 2, id="v001"),
    pytest.param((1, 0, 2, 3), 3, id="v002"),
    pytest.param((1, 2, 2, 3), 5, id="v003"),
])
def test_renamed_values(args,expected):
    actual=row_major_offset(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 2, 3), id="e022"),
    pytest.param((2, 0, 2, 3), id="e023"),
    pytest.param((0, 3, 2, 3), id="e024"),
])
def test_renamed_raises_indexerror(args):
    with pytest.raises(IndexError):
        row_major_offset(*args)

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
    pytest.param((IntChild(0), 0, 0, 2), id="e025"),
    pytest.param((0, IntChild(0), 0, 2), id="e026"),
    pytest.param((0, 0, IntChild(0), 2), id="e027"),
    pytest.param((0, 0, 0, IntChild(2)), id="e028"),
    pytest.param((IntChild(0), 0, 2, 0), id="e029"),
    pytest.param((0, IntChild(0), 2, 0), id="e030"),
    pytest.param((0, 0, IntChild(2), 0), id="e031"),
    pytest.param((0, 0, 2, IntChild(0)), id="e032"),
    pytest.param((IntChild(-1), 0, 2, 3), id="e033"),
    pytest.param((-1, IntChild(0), 2, 3), id="e034"),
    pytest.param((-1, 0, IntChild(2), 3), id="e035"),
    pytest.param((-1, 0, 2, IntChild(3)), id="e036"),
    pytest.param((IntChild(2), 0, 2, 3), id="e037"),
    pytest.param((2, IntChild(0), 2, 3), id="e038"),
    pytest.param((2, 0, IntChild(2), 3), id="e039"),
    pytest.param((2, 0, 2, IntChild(3)), id="e040"),
    pytest.param((IntChild(0), 3, 2, 3), id="e041"),
    pytest.param((0, IntChild(3), 2, 3), id="e042"),
    pytest.param((0, 3, IntChild(2), 3), id="e043"),
    pytest.param((0, 3, 2, IntChild(3)), id="e044"),
])
def test_renamed_raises_typeerror(args):
    with pytest.raises(TypeError):
        row_major_offset(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 0, 2), id="e020"),
    pytest.param((0, 0, 2, 0), id="e021"),
])
def test_renamed_raises_valueerror(args):
    with pytest.raises(ValueError):
        row_major_offset(*args)
