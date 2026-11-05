import copy
import pytest
from subject import make_slug
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
    pytest.param((' --_ ',), ''),
    pytest.param(('Hello World',), 'hello-world'),
    pytest.param((' A__b--C ',), 'a-b-c'),
    pytest.param(('X9',), 'x9'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=make_slug(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild('a/b'),)),
    pytest.param((StrChild('é'),)),
    pytest.param((StrChild('a\tb'),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        make_slug(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('a/b',)),
    pytest.param(('é',)),
    pytest.param(('a\tb',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        make_slug(*args)
