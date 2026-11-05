import copy
import pytest
from subject import quote_csv_field
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
    pytest.param(('',), '""'),
    pytest.param(('abc',), 'abc'),
    pytest.param(('a,b',), '"a,b"'),
    pytest.param(('a"b',), '"a""b"'),
    pytest.param(('a\rb',), '"a\rb"'),
    pytest.param(('a\nb',), '"a\nb"'),
    pytest.param((' a ',), ' a '),
    pytest.param(('é',), 'é'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=quote_csv_field(*args)
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
        quote_csv_field(*args)
