import copy
import pytest
from subject import merge_sorted

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
    pytest.param(([], []), [], id="v000"),
    pytest.param(([1], []), [1], id="v001"),
    pytest.param(([], [1]), [1], id="v002"),
    pytest.param(([1, 3], [2, 4]), [1, 2, 3, 4], id="v003"),
    pytest.param(([1, 1, 3], [1, 2]), [1, 1, 1, 2, 3], id="v004"),
    pytest.param(([-3, 0], [-2, 0]), [-3, -2, 0, 0], id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=merge_sorted(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), []), id="e000"),
    pytest.param(([True], []), id="e001"),
    pytest.param(([IntChild(1)], []), id="e002"),
    pytest.param(((), []), id="e003"),
    pytest.param((None, []), id="e004"),
    pytest.param(([], ListChild([])), id="e005"),
    pytest.param(([], [True]), id="e006"),
    pytest.param(([], [IntChild(1)]), id="e007"),
    pytest.param(([], ()), id="e008"),
    pytest.param(([], None), id="e009"),
    pytest.param(([2, 1], ListChild([])), id="e012"),
    pytest.param((ListChild([]), [1, 0]), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        merge_sorted(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([2, 1], []), id="e010"),
    pytest.param(([], [1, 0]), id="e011"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        merge_sorted(*args)
