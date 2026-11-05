import copy
import pytest
from subject import lower_median
class IntChild(int): pass
class ListChild(list): pass
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
    pytest.param(([1],), 1),
    pytest.param(([4, 1],), 1),
    pytest.param(([9, 1, 5],), 5),
    pytest.param(([9, 1, 5, 3],), 3),
    pytest.param(([-1, -1, 0],), -1),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=lower_median(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([1]),)),
    pytest.param(([True],)),
    pytest.param(([IntChild(1)],)),
    pytest.param(((),)),
    pytest.param((None,)),
    pytest.param((ListChild([]),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        lower_median(*args)
@pytest.mark.parametrize("args", [
    pytest.param(([],)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        lower_median(*args)
