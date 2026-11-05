import copy
import pytest
from subject import prefix_sums
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
    pytest.param(([],), []),
    pytest.param(([5],), [5]),
    pytest.param(([1, 2, 3],), [1, 3, 6]),
    pytest.param(([-1, 2, -3],), [-1, 1, -2]),
    pytest.param(([0, 0],), [0, 0]),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=prefix_sums(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),)),
    pytest.param(([True],)),
    pytest.param(([IntChild(1)],)),
    pytest.param(((),)),
    pytest.param((None,)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        prefix_sums(*args)
