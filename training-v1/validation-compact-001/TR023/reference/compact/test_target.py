import copy
import pytest
from subject import plural_count
class IntChild(int): pass
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
    pytest.param((0, 'cat'), '0 cats'),
    pytest.param((1, 'cat'), '1 cat'),
    pytest.param((2, 'cat'), '2 cats'),
    pytest.param((1, 'box'), '1 box'),
    pytest.param((2, 'box'), '2 boxs'),
    pytest.param((10, 'é'), '10 és'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=plural_count(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 'cat')),
    pytest.param((IntChild(0), 'cat')),
    pytest.param((1.5, 'cat')),
    pytest.param(('bad', 'cat')),
    pytest.param((None, 'cat')),
    pytest.param((0, StrChild('cat'))),
    pytest.param((0, b'x')),
    pytest.param((0, 1)),
    pytest.param((0, None)),
    pytest.param((IntChild(-1), 'cat')),
    pytest.param((-1, StrChild('cat'))),
    pytest.param((IntChild(1), '')),
    pytest.param((1, StrChild(''))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        plural_count(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1, 'cat')),
    pytest.param((1, '')),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        plural_count(*args)
