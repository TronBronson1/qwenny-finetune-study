import pytest
from subject import absolute_distance

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0, 0), 0, id="v000"),
    pytest.param((1, 0), 1, id="v001"),
    pytest.param((0, 1), 1, id="v002"),
    pytest.param((-3, 5), 8, id="v003"),
    pytest.param((5, -3), 8, id="v004"),
    pytest.param((-8, -2), 6, id="v005"),
    pytest.param((100000000000000000000, -100000000000000000000), 200000000000000000000, id="v006"),
])
def test_values(args,expected):
    actual=absolute_distance(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True, 0), id="e000"),
    pytest.param((IntChild(0), 0), id="e001"),
    pytest.param((1.5, 0), id="e002"),
    pytest.param(('bad', 0), id="e003"),
    pytest.param((None, 0), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(0)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        absolute_distance(*args)
