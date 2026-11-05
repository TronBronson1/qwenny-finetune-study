import copy
import pytest
from subject import chunk_list
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
    pytest.param(([], 2), []),
    pytest.param(([1], 2), [[1]]),
    pytest.param(([1, 2, 3, 4], 2), [[1, 2], [3, 4]]),
    pytest.param(([1, 2, 3], 2), [[1, 2], [3]]),
    pytest.param(([1, 2], 1), [[1], [2]]),
    pytest.param(([1, 2], 9), [[1, 2]]),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=chunk_list(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 2)),
    pytest.param(([True], 2)),
    pytest.param(([IntChild(1)], 2)),
    pytest.param(((), 2)),
    pytest.param((None, 2)),
    pytest.param(([], True)),
    pytest.param(([], IntChild(2))),
    pytest.param(([], 1.5)),
    pytest.param(([], 'bad')),
    pytest.param(([], None)),
    pytest.param((ListChild([1]), 0)),
    pytest.param(([1], IntChild(0))),
    pytest.param((ListChild([]), -1)),
    pytest.param(([], IntChild(-1))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        chunk_list(*args)
@pytest.mark.parametrize("args", [
    pytest.param(([1], 0)),
    pytest.param(([], -1)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        chunk_list(*args)
