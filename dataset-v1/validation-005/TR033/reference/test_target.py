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
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param(([1], 0), [], id="v000"),
    pytest.param(([1, 2, 3], 0), [2, 3], id="v001"),
    pytest.param(([1, 2, 3], 1), [1, 3], id="v002"),
    pytest.param(([1, 2, 3], 2), [1, 2], id="v003"),
    pytest.param(([2, 2], 1), [2], id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=remove_at(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([], 0), id="e010"),
    pytest.param(([1], -1), id="e011"),
    pytest.param(([1], 1), id="e012"),
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
    pytest.param(([1], True), id="e005"),
    pytest.param(([1], IntChild(0)), id="e006"),
    pytest.param(([1], 1.5), id="e007"),
    pytest.param(([1], 'bad'), id="e008"),
    pytest.param(([1], None), id="e009"),
    pytest.param(([], True), id="e013"),
    pytest.param((ListChild([1]), -1), id="e014"),
    pytest.param((ListChild([1]), 1), id="e015"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        remove_at(*args)
