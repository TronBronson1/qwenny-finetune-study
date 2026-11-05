import copy
import pytest
from subject import transpose
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
    pytest.param(([[]],), []),
    pytest.param(([[], []],), []),
    pytest.param(([[1, 2], [3, 4]],), [[1, 3], [2, 4]]),
    pytest.param(([[1, 2, 3]],), [[1], [2], [3]]),
    pytest.param(([[1], [2], [3]],), [[1, 2, 3]]),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=transpose(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),)),
    pytest.param(([ListChild([1])],)),
    pytest.param(([[True]],)),
    pytest.param(([[IntChild(1)]],)),
    pytest.param((['x'],)),
    pytest.param((None,)),
    pytest.param((ListChild([[1], [2, 3]]),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        transpose(*args)
@pytest.mark.parametrize("args", [
    pytest.param(([[1], [2, 3]],)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        transpose(*args)
