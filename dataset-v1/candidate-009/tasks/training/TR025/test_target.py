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

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param((['a'],), [('a', 1)], id="v001"),
    pytest.param((['a', 'a', 'b', 'a'],), [('a', 2), ('b', 1), ('a', 1)], id="v002"),
    pytest.param((['', '', 'x'],), [('', 2), ('x', 1)], id="v003"),
    pytest.param((['A', 'a'],), [('A', 1), ('a', 1)], id="v004"),
    pytest.param((['é', 'é', '字'],), [('é', 2), ('字', 1)], id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=run_length_encode(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([StrChild('x')],), id="e001"),
    pytest.param(([1],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        run_length_encode(*args)
    assert args == before
