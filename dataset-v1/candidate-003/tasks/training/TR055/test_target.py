import copy
import pytest
from subject import encode_rgb

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
    pytest.param((0, 0, 0), '#000000', (0, 0, 0), id="v000"),
    pytest.param((255, 255, 255), '#ffffff', (255, 255, 255), id="v001"),
    pytest.param((1, 2, 3), '#010203', (1, 2, 3), id="v002"),
    pytest.param((0, 128, 255), '#0080ff', (0, 128, 255), id="v003"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=encode_rgb(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 0), id="e000"),
    pytest.param((IntChild(0), 0, 0), id="e001"),
    pytest.param((1.5, 0, 0), id="e002"),
    pytest.param(('bad', 0, 0), id="e003"),
    pytest.param((None, 0, 0), id="e004"),
    pytest.param((0, True, 0), id="e005"),
    pytest.param((0, IntChild(0), 0), id="e006"),
    pytest.param((0, 1.5, 0), id="e007"),
    pytest.param((0, 'bad', 0), id="e008"),
    pytest.param((0, None, 0), id="e009"),
    pytest.param((0, 0, True), id="e010"),
    pytest.param((0, 0, IntChild(0)), id="e011"),
    pytest.param((0, 0, 1.5), id="e012"),
    pytest.param((0, 0, 'bad'), id="e013"),
    pytest.param((0, 0, None), id="e014"),
    pytest.param((-1, True, 0), id="e018"),
    pytest.param((True, 256, 0), id="e019"),
    pytest.param((True, 0, -1), id="e020"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        encode_rgb(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 0), id="e015"),
    pytest.param((0, 256, 0), id="e016"),
    pytest.param((0, 0, -1), id="e017"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        encode_rgb(*args)
