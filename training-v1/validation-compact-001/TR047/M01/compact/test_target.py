import copy
import pytest
from subject import index_of_nth
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
    pytest.param(('', 'a', 1), -1),
    pytest.param(('aaaa', 'aa', 1), 0),
    pytest.param(('aaaa', 'aa', 2), 1),
    pytest.param(('aaaa', 'aa', 3), 2),
    pytest.param(('aaaa', 'aa', 4), -1),
    pytest.param(('abc', 'abc', 1), 0),
    pytest.param(('abc', 'x', 1), -1),
    pytest.param(('éé', 'é', 2), 1),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=index_of_nth(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''), 'a', 1)),
    pytest.param((b'x', 'a', 1)),
    pytest.param((1, 'a', 1)),
    pytest.param((None, 'a', 1)),
    pytest.param(('', StrChild('a'), 1)),
    pytest.param(('', b'x', 1)),
    pytest.param(('', 1, 1)),
    pytest.param(('', None, 1)),
    pytest.param(('', 'a', True)),
    pytest.param(('', 'a', IntChild(1))),
    pytest.param(('', 'a', 1.5)),
    pytest.param(('', 'a', 'bad')),
    pytest.param(('', 'a', None)),
    pytest.param((StrChild('abc'), '', 1)),
    pytest.param(('abc', StrChild(''), 1)),
    pytest.param(('abc', '', IntChild(1))),
    pytest.param((StrChild('abc'), 'a', 0)),
    pytest.param(('abc', StrChild('a'), 0)),
    pytest.param(('abc', 'a', IntChild(0))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        index_of_nth(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('abc', '', 1)),
    pytest.param(('abc', 'a', 0)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        index_of_nth(*args)
