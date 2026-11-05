import copy
import pytest
from subject import collapse_spaces
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
    pytest.param(('',), ''),
    pytest.param(('a',), 'a'),
    pytest.param(('   ',), ' '),
    pytest.param((' a  b ',), ' a b '),
    pytest.param(('a\t  b',), 'a\t b'),
    pytest.param(('a\n  b',), 'a\n b'),
    pytest.param(('é  字',), 'é 字'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=collapse_spaces(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        collapse_spaces(*args)
