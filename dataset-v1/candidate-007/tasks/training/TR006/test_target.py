import pytest
from subject import factorial

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), 1, id="v000"),
    pytest.param((1,), 1, id="v001"),
    pytest.param((2,), 2, id="v002"),
    pytest.param((5,), 120, id="v003"),
    pytest.param((12,), 479001600, id="v004"),
])
def test_values(args,expected):
    actual=factorial(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((IntChild(-1),), id="e007"),
    pytest.param((IntChild(13),), id="e008"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        factorial(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1,), id="e005"),
    pytest.param((13,), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        factorial(*args)
