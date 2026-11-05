import copy
import pytest
from subject import encode_rgb
class IntChild(int): pass
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
    pytest.param((0, 0, 0), '#000000'),
    pytest.param((255, 255, 255), '#ffffff'),
    pytest.param((1, 2, 3), '#010203'),
    pytest.param((0, 128, 255), '#0080ff'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=encode_rgb(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 0, 0)),
    pytest.param((IntChild(0), 0, 0)),
    pytest.param((1.5, 0, 0)),
    pytest.param(('bad', 0, 0)),
    pytest.param((None, 0, 0)),
    pytest.param((0, True, 0)),
    pytest.param((0, IntChild(0), 0)),
    pytest.param((0, 1.5, 0)),
    pytest.param((0, 'bad', 0)),
    pytest.param((0, None, 0)),
    pytest.param((0, 0, True)),
    pytest.param((0, 0, IntChild(0))),
    pytest.param((0, 0, 1.5)),
    pytest.param((0, 0, 'bad')),
    pytest.param((0, 0, None)),
    pytest.param((IntChild(-1), 0, 0)),
    pytest.param((-1, IntChild(0), 0)),
    pytest.param((-1, 0, IntChild(0))),
    pytest.param((IntChild(0), 256, 0)),
    pytest.param((0, IntChild(256), 0)),
    pytest.param((0, 256, IntChild(0))),
    pytest.param((IntChild(0), 0, -1)),
    pytest.param((0, IntChild(0), -1)),
    pytest.param((0, 0, IntChild(-1))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        encode_rgb(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1, 0, 0)),
    pytest.param((0, 256, 0)),
    pytest.param((0, 0, -1)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        encode_rgb(*args)
