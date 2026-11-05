import copy
import pytest
from subject import unravel_index

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
    pytest.param((0, 1, 1), (0, 0), (0, 1, 1), id="v000"),
    pytest.param((0, 2, 3), (0, 0), (0, 2, 3), id="v001"),
    pytest.param((2, 2, 3), (0, 2), (2, 2, 3), id="v002"),
    pytest.param((3, 2, 3), (1, 0), (3, 2, 3), id="v003"),
    pytest.param((5, 2, 3), (1, 2), (5, 2, 3), id="v004"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=unravel_index(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((-1, 2, 3), id="e016"),
    pytest.param((6, 2, 3), id="e017"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        unravel_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((True, 1, 1), id="e000"),
    pytest.param((IntChild(0), 1, 1), id="e001"),
    pytest.param((1.5, 1, 1), id="e002"),
    pytest.param(('bad', 1, 1), id="e003"),
    pytest.param((None, 1, 1), id="e004"),
    pytest.param((0, True, 1), id="e005"),
    pytest.param((0, IntChild(1), 1), id="e006"),
    pytest.param((0, 1.5, 1), id="e007"),
    pytest.param((0, 'bad', 1), id="e008"),
    pytest.param((0, None, 1), id="e009"),
    pytest.param((0, 1, True), id="e010"),
    pytest.param((0, 1, IntChild(1)), id="e011"),
    pytest.param((0, 1, 1.5), id="e012"),
    pytest.param((0, 1, 'bad'), id="e013"),
    pytest.param((0, 1, None), id="e014"),
    pytest.param((True, 0, 2), id="e018"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        unravel_index(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0, 0, 2), id="e015"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        unravel_index(*args)
