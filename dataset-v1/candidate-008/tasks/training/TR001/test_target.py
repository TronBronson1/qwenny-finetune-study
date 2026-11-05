import pytest
from subject import batches

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 3), 0, id="v000"),
    pytest.param((1, 3), 1, id="v001"),
    pytest.param((3, 3), 1, id="v002"),
    pytest.param((4, 3), 2, id="v003"),
    pytest.param((7, 1), 7, id="v004"),
    pytest.param((1000000000000000000000000000000, 3), 333333333333333333333333333334, id="v005"),
])
def test_values(args,expected):
    actual=batches(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 3), id="e000"),
    pytest.param((IntChild(0), 3), id="e001"),
    pytest.param((1.5, 3), id="e002"),
    pytest.param(('bad', 3), id="e003"),
    pytest.param((None, 3), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(3)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
    pytest.param(('bad', 0), id="e013"),
    pytest.param((-1, 'bad'), id="e014"),
    pytest.param((IntChild(-1), 3), id="e015"),
    pytest.param((-1, IntChild(3)), id="e016"),
    pytest.param((IntChild(2), 0), id="e017"),
    pytest.param((2, IntChild(0)), id="e018"),
    pytest.param((IntChild(2), -1), id="e019"),
    pytest.param((2, IntChild(-1)), id="e020"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        batches(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 3), id="e010"),
    pytest.param((2, 0), id="e011"),
    pytest.param((2, -1), id="e012"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        batches(*args)
