import copy
import pytest
from subject import leap_year

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
    pytest.param((1,), False, id="v000"),
    pytest.param((4,), True, id="v001"),
    pytest.param((1900,), False, id="v002"),
    pytest.param((2000,), True, id="v003"),
    pytest.param((2023,), False, id="v004"),
    pytest.param((2024,), True, id="v005"),
    pytest.param((2100,), False, id="v006"),
    pytest.param((9999,), False, id="v007"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=leap_year(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(1),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        leap_year(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0,), id="e005"),
    pytest.param((10000,), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        leap_year(*args)
