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

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), [], id="v000"),
    pytest.param(([[]],), [], id="v001"),
    pytest.param(([[], []],), [], id="v002"),
    pytest.param(([[1, 2], [3, 4]],), [[1, 3], [2, 4]], id="v003"),
    pytest.param(([[1, 2, 3]],), [[1], [2], [3]], id="v004"),
    pytest.param(([[1], [2], [3]],), [[1, 2, 3]], id="v005"),
    pytest.param(([[2, 1], [0, 3]],), [[2, 0], [1, 3]], id="v006"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=transpose(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]),), id="e000"),
    pytest.param(([ListChild([1])],), id="e001"),
    pytest.param(([[True]],), id="e002"),
    pytest.param(([[IntChild(1)]],), id="e003"),
    pytest.param((['x'],), id="e004"),
    pytest.param((None,), id="e005"),
    pytest.param(([['x']],), id="e006"),
    pytest.param(([[1.5]],), id="e007"),
    pytest.param(([[None]],), id="e008"),
    pytest.param(([1],), id="e009"),
    pytest.param(((),), id="e011"),
    pytest.param(([(1,)],), id="e012"),
    pytest.param(([[1], None, [1, 2]],), id="e013"),
    pytest.param((ListChild([[1], [2, 3]]),), id="e014"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        transpose(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([[1], [2, 3]],), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        transpose(*args)
