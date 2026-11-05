import copy
import pytest
from subject import run_length_encode

class IntChild(int): pass
class StrChild(str): pass
class BytesChild(bytes): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected,after", [
    pytest.param(([],), [], ([],), id="v000"),
    pytest.param((['a'],), [('a', 1)], (['a'],), id="v001"),
    pytest.param((['a', 'a', 'b', 'a'],), [('a', 2), ('b', 1), ('a', 1)], (['a', 'a', 'b', 'a'],), id="v002"),
    pytest.param((['', '', 'x'],), [('', 2), ('x', 1)], (['', '', 'x'],), id="v003"),
    pytest.param((['A', 'a'],), [('A', 1), ('a', 1)], (['A', 'a'],), id="v004"),
    pytest.param((['é', 'é', '字'],), [('é', 2), ('字', 1)], (['é', 'é', '字'],), id="v005"),
])
def test_values(args,expected,after):
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
    with pytest.raises(TypeError):
        run_length_encode(*args)
