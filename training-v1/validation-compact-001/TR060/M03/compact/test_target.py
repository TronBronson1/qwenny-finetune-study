import copy
import pytest
from subject import count_ascii_categories
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
    pytest.param(('',), (0, 0, 0)),
    pytest.param(('AbZz09',), (4, 2, 0)),
    pytest.param(('a 1!',), (1, 1, 2)),
    pytest.param(('é١',), (0, 0, 2)),
    pytest.param(('\n\t',), (0, 0, 2)),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=count_ascii_categories(*args)
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
        count_ascii_categories(*args)
