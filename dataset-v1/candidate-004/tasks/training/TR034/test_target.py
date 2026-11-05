import copy
import pytest
from subject import bounded_slice

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
    pytest.param(([], 0, 0), [], ([], 0, 0), id="v000"),
    pytest.param(([1, 2, 3], 0, 3), [1, 2, 3], ([1, 2, 3], 0, 3), id="v001"),
    pytest.param(([1, 2, 3], 1, 2), [2], ([1, 2, 3], 1, 2), id="v002"),
    pytest.param(([1, 2, 3], 2, 1), [], ([1, 2, 3], 2, 1), id="v003"),
    pytest.param(([1, 2, 3], 3, 3), [], ([1, 2, 3], 3, 3), id="v004"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=bounded_slice(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param(([1], -1, 1), id="e015"),
    pytest.param(([1], 0, 2), id="e016"),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        bounded_slice(*args)

@pytest.mark.parametrize("args", [
    pytest.param((ListChild([]), 0, 0), id="e000"),
    pytest.param(([True], 0, 0), id="e001"),
    pytest.param(([IntChild(1)], 0, 0), id="e002"),
    pytest.param(((), 0, 0), id="e003"),
    pytest.param((None, 0, 0), id="e004"),
    pytest.param(([], True, 0), id="e005"),
    pytest.param(([], IntChild(0), 0), id="e006"),
    pytest.param(([], 1.5, 0), id="e007"),
    pytest.param(([], 'bad', 0), id="e008"),
    pytest.param(([], None, 0), id="e009"),
    pytest.param(([], 0, True), id="e010"),
    pytest.param(([], 0, IntChild(0)), id="e011"),
    pytest.param(([], 0, 1.5), id="e012"),
    pytest.param(([], 0, 'bad'), id="e013"),
    pytest.param(([], 0, None), id="e014"),
    pytest.param(([1], True, 2), id="e017"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        bounded_slice(*args)
