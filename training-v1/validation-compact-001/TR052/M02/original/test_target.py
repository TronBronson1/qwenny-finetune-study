import copy
import pytest
from subject import seconds_to_hms

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
    pytest.param((0,), (0, 0, 0), id="v000"),
    pytest.param((59,), (0, 0, 59), id="v001"),
    pytest.param((60,), (0, 1, 0), id="v002"),
    pytest.param((3599,), (0, 59, 59), id="v003"),
    pytest.param((3600,), (1, 0, 0), id="v004"),
    pytest.param((90061,), (25, 1, 1), id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=seconds_to_hms(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((IntChild(-1),), id="e006"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        seconds_to_hms(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1,), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        seconds_to_hms(*args)
