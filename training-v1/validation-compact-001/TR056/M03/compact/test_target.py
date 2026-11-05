import copy
import pytest
from subject import decode_rgb
class StrChild(str): pass
def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])
@pytest.mark.parametrize("args,expected", [
    pytest.param(('#000000',), (0, 0, 0)),
    pytest.param(('#ffffff',), (255, 255, 255)),
    pytest.param(('#010203',), (1, 2, 3)),
    pytest.param(('#00aAFF',), (0, 170, 255)),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=decode_rgb(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('#000000'),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild('ffffff'),)),
    pytest.param((StrChild('#fff'),)),
    pytest.param((StrChild('#gg0000'),)),
    pytest.param((StrChild('#000000\n'),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        decode_rgb(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('ffffff',)),
    pytest.param(('#fff',)),
    pytest.param(('#gg0000',)),
    pytest.param(('#000000\n',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        decode_rgb(*args)
