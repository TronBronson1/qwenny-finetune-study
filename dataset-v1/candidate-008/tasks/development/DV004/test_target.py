import copy
import pytest
from subject import xor_checksum

class IntChild(int): pass
class ListChild(list): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(([],), 0, id="v000"),
    pytest.param(([0],), 0, id="v001"),
    pytest.param(([255],), 255, id="v002"),
    pytest.param(([1, 2, 3],), 0, id="v003"),
    pytest.param(([5, 5],), 0, id="v004"),
    pytest.param(([128, 1, 128],), 1, id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=xor_checksum(*args)
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
    pytest.param(([-1, 'x'],), id="e011"),
    pytest.param((ListChild([-1]),), id="e012"),
    pytest.param((ListChild([256]),), id="e013"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        xor_checksum(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([-1],), id="e009"),
    pytest.param(([256],), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        xor_checksum(*args)
