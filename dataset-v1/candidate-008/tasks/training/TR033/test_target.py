import copy
import pytest
from subject import remove_at

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([1], 0), [], id="v000"),
    pytest.param(([1, 2, 3], 0), [2, 3], id="v001"),
    pytest.param(([1, 2, 3], 1), [1, 3], id="v002"),
    pytest.param(([1, 2, 3], 2), [1, 2], id="v003"),
    pytest.param(([2, 2], 1), [2], id="v004"),
    pytest.param(([4, 2], 0), [2], id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=remove_at(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([], 0), id="e014"),
    pytest.param(([1], -1), id="e015"),
    pytest.param(([1], 1), id="e016"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        remove_at(*args)

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([1]), 0), id="e000"),
    pytest.param(([True], 0), id="e001"),
    pytest.param(([IntChild(1)], 0), id="e002"),
    pytest.param(((), 0), id="e003"),
    pytest.param((None, 0), id="e004"),
    pytest.param((['x'], 0), id="e005"),
    pytest.param(([1.5], 0), id="e006"),
    pytest.param(([-1.5], 0), id="e007"),
    pytest.param(([None], 0), id="e008"),
    pytest.param(([1], True), id="e009"),
    pytest.param(([1], IntChild(0)), id="e010"),
    pytest.param(([1], 1.5), id="e011"),
    pytest.param(([1], 'bad'), id="e012"),
    pytest.param(([1], None), id="e013"),
    pytest.param((ListChild([]), 0), id="e017"),
    pytest.param(([], IntChild(0)), id="e018"),
    pytest.param((ListChild([1]), -1), id="e019"),
    pytest.param(([1], IntChild(-1)), id="e020"),
    pytest.param((ListChild([1]), 1), id="e021"),
    pytest.param(([1], IntChild(1)), id="e022"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        remove_at(*args)
