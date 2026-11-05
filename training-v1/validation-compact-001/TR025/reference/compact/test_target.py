import copy
import pytest
from subject import run_length_encode
class StrChild(str): pass
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
    pytest.param((['a'],), [('a', 1)]),
    pytest.param((['a', 'a', 'b', 'a'],), [('a', 2), ('b', 1), ('a', 1)]),
    pytest.param((['', '', 'x'],), [('', 2), ('x', 1)]),
    pytest.param((['A', 'a'],), [('A', 1), ('a', 1)]),
    pytest.param((['é', 'é', '字'],), [('é', 2), ('字', 1)]),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=run_length_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),)),
    pytest.param(([StrChild('x')],)),
    pytest.param(([1],)),
    pytest.param(((),)),
    pytest.param((None,)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        run_length_encode(*args)
