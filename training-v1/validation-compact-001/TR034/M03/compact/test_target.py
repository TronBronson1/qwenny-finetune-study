import copy
import pytest
from subject import bounded_slice
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
    pytest.param(([], 0, 0), []),
    pytest.param(([1, 2, 3], 0, 3), [1, 2, 3]),
    pytest.param(([1, 2, 3], 1, 2), [2]),
    pytest.param(([1, 2, 3], 2, 1), []),
    pytest.param(([1, 2, 3], 3, 3), []),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=bounded_slice(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param(([1], -1, 1)),
    pytest.param(([1], 0, 2)),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        bounded_slice(*args)
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 0, 0)),
    pytest.param(([True], 0, 0)),
    pytest.param(([IntChild(1)], 0, 0)),
    pytest.param(((), 0, 0)),
    pytest.param((None, 0, 0)),
    pytest.param(([], True, 0)),
    pytest.param(([], IntChild(0), 0)),
    pytest.param(([], 1.5, 0)),
    pytest.param(([], 'bad', 0)),
    pytest.param(([], None, 0)),
    pytest.param(([], 0, True)),
    pytest.param(([], 0, IntChild(0))),
    pytest.param(([], 0, 1.5)),
    pytest.param(([], 0, 'bad')),
    pytest.param(([], 0, None)),
    pytest.param((ListChild([1]), -1, 1)),
    pytest.param(([1], IntChild(-1), 1)),
    pytest.param(([1], -1, IntChild(1))),
    pytest.param((ListChild([1]), 0, 2)),
    pytest.param(([1], IntChild(0), 2)),
    pytest.param(([1], 0, IntChild(2))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        bounded_slice(*args)
