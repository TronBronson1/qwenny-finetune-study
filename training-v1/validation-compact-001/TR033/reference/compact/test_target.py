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
    pytest.param(([1], 0), []),
    pytest.param(([1, 2, 3], 0), [2, 3]),
    pytest.param(([1, 2, 3], 1), [1, 3]),
    pytest.param(([1, 2, 3], 2), [1, 2]),
    pytest.param(([2, 2], 1), [2]),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=remove_at(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param(([], 0)),
    pytest.param(([1], -1)),
    pytest.param(([1], 1)),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        remove_at(*args)
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([1]), 0)),
    pytest.param(([True], 0)),
    pytest.param(([IntChild(1)], 0)),
    pytest.param(((), 0)),
    pytest.param((None, 0)),
    pytest.param(([1], True)),
    pytest.param(([1], IntChild(0))),
    pytest.param(([1], 1.5)),
    pytest.param(([1], 'bad')),
    pytest.param(([1], None)),
    pytest.param((ListChild([]), 0)),
    pytest.param(([], IntChild(0))),
    pytest.param((ListChild([1]), -1)),
    pytest.param(([1], IntChild(-1))),
    pytest.param((ListChild([1]), 1)),
    pytest.param(([1], IntChild(1))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        remove_at(*args)
