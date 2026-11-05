import copy
import pytest
from subject import signed_gcd

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
    pytest.param((0, 0), 0, (0, 0), id="v000"),
    pytest.param((0, 8), 8, (0, 8), id="v001"),
    pytest.param((8, 0), 8, (8, 0), id="v002"),
    pytest.param((18, 12), 6, (18, 12), id="v003"),
    pytest.param((-18, 12), 6, (-18, 12), id="v004"),
    pytest.param((18, -12), 6, (18, -12), id="v005"),
    pytest.param((-18, -12), 6, (-18, -12), id="v006"),
    pytest.param((7, 13), 1, (7, 13), id="v007"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=signed_gcd(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True, 0), id="e000"),
    pytest.param((IntChild(0), 0), id="e001"),
    pytest.param((1.5, 0), id="e002"),
    pytest.param(('bad', 0), id="e003"),
    pytest.param((None, 0), id="e004"),
    pytest.param((0, True), id="e005"),
    pytest.param((0, IntChild(0)), id="e006"),
    pytest.param((0, 1.5), id="e007"),
    pytest.param((0, 'bad'), id="e008"),
    pytest.param((0, None), id="e009"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        signed_gcd(*args)
