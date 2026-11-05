import copy
import pytest
from subject import strip_prefix
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
    pytest.param(('abc', 'a'), 'bc'),
    pytest.param(('abc', 'abc'), ''),
    pytest.param(('abc', 'z'), 'abc'),
    pytest.param(('', 'a'), ''),
    pytest.param(('aaaa', 'a'), 'aaa'),
    pytest.param(('Abc', 'a'), 'Abc'),
    pytest.param(('ba', 'a'), 'ba'),
    pytest.param((' ab', ' '), 'ab'),
    pytest.param(('éclair', 'é'), 'clair'),
    pytest.param(('abc', 'abcd'), 'abc'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=strip_prefix(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('abc'), 'a')),
    pytest.param((b'x', 'a')),
    pytest.param((1, 'a')),
    pytest.param((None, 'a')),
    pytest.param(('abc', StrChild('a'))),
    pytest.param(('abc', b'x')),
    pytest.param(('abc', 1)),
    pytest.param(('abc', None)),
    pytest.param((StrChild('abc'), '')),
    pytest.param(('abc', StrChild(''))),
    pytest.param((StrChild(''), '')),
    pytest.param(('', StrChild(''))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        strip_prefix(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('abc', '')),
    pytest.param(('', '')),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        strip_prefix(*args)
