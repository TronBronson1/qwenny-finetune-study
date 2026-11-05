import copy
import pytest
from subject import pairwise_differences

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
    pytest.param(([],), [], id="v000"),
    pytest.param(([4],), [], id="v001"),
    pytest.param(([1, 4, 2],), [3, -2], id="v002"),
    pytest.param(([3, 3],), [0], id="v003"),
    pytest.param(([-2, -5, 1],), [-3, 6], id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=pairwise_differences(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([True],), id="e001"),
    pytest.param(([IntChild(1)],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        pairwise_differences(*args)
