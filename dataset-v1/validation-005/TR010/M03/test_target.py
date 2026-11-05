import copy
import pytest
from subject import population_count

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), 0, id="v000"),
    pytest.param((1,), 1, id="v001"),
    pytest.param((2,), 1, id="v002"),
    pytest.param((3,), 2, id="v003"),
    pytest.param((255,), 8, id="v004"),
    pytest.param((256,), 1, id="v005"),
    pytest.param((1267650600228229401496703205377,), 2, id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=population_count(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        population_count(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1,), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        population_count(*args)
