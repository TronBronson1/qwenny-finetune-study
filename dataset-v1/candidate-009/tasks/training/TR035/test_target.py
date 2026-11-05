import copy
import pytest
from subject import adjacent_equal_count

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), 0, id="v000"),
    pytest.param(([1],), 0, id="v001"),
    pytest.param(([1, 1],), 1, id="v002"),
    pytest.param(([1, 1, 1],), 2, id="v003"),
    pytest.param(([1, 2, 1],), 0, id="v004"),
    pytest.param(([1, 1, 2, 2, 2],), 3, id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=adjacent_equal_count(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([True],), id="e001"),
    pytest.param(([IntChild(1)],), id="e002"),
    pytest.param(((),), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((['x'],), id="e005"),
    pytest.param(([1.5],), id="e006"),
    pytest.param(([-1.5],), id="e007"),
    pytest.param(([None],), id="e008"),
])
def test_raises_typeerror(args):
    before=copy.deepcopy(args)
    with pytest.raises(TypeError):
        adjacent_equal_count(*args)
    assert args == before
