import copy
import pytest
from subject import multiset_intersection

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([], []), [], id="v000"),
    pytest.param(([1], []), [], id="v001"),
    pytest.param(([], [1]), [], id="v002"),
    pytest.param(([2, 1, 2, 3], [2, 2, 4]), [2, 2], id="v003"),
    pytest.param(([1, 1, 1], [1, 1]), [1, 1], id="v004"),
    pytest.param(([-1, 0, -1], [0, -1]), [-1, 0], id="v005"),
    pytest.param(([2, 1, 2], [1, 2]), [2, 1], id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=multiset_intersection(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), []), id="e000"),
    pytest.param(([True], []), id="e001"),
    pytest.param(([IntChild(1)], []), id="e002"),
    pytest.param(((), []), id="e003"),
    pytest.param((None, []), id="e004"),
    pytest.param((['x'], []), id="e005"),
    pytest.param(([1.5], []), id="e006"),
    pytest.param(([-1.5], []), id="e007"),
    pytest.param(([None], []), id="e008"),
    pytest.param(([], ListChild([])), id="e009"),
    pytest.param(([], [True]), id="e010"),
    pytest.param(([], [IntChild(1)]), id="e011"),
    pytest.param(([], ()), id="e012"),
    pytest.param(([], None), id="e013"),
    pytest.param(([], ['x']), id="e014"),
    pytest.param(([], [1.5]), id="e015"),
    pytest.param(([], [-1.5]), id="e016"),
    pytest.param(([], [None]), id="e017"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        multiset_intersection(*args)
