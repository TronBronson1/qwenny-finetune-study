import copy
import pytest
from subject import xor_checksum

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
    pytest.param(([],), 0, ([],), id="v000"),
    pytest.param(([0],), 0, ([0],), id="v001"),
    pytest.param(([255],), 255, ([255],), id="v002"),
    pytest.param(([1, 2, 3],), 0, ([1, 2, 3],), id="v003"),
    pytest.param(([5, 5],), 0, ([5, 5],), id="v004"),
    pytest.param(([128, 1, 128],), 1, ([128, 1, 128],), id="v005"),
])
def test_values(args,expected,after):
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
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        xor_checksum(*args)

@pytest.mark.parametrize("args", [
    pytest.param(([-1],), id="e005"),
    pytest.param(([256],), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        xor_checksum(*args)
