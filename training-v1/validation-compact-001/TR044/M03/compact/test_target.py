import copy
import pytest
from subject import parse_range
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
    pytest.param(('[0:0]',), (0, 0)),
    pytest.param(('[0:99]',), (0, 99)),
    pytest.param(('[3:7]',), (3, 7)),
    pytest.param(('[99:99]',), (99, 99)),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_range(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild('[0:0]'),)),
    pytest.param((b'x',)),
    pytest.param((1,)),
    pytest.param((None,)),
    pytest.param((StrChild('[7:3]'),)),
    pytest.param((StrChild('0:1'),)),
    pytest.param((StrChild('[00:1]'),)),
    pytest.param((StrChild('[0:100]'),)),
    pytest.param((StrChild('[0:1] '),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_range(*args)
@pytest.mark.parametrize("args", [
    pytest.param(('[7:3]',)),
    pytest.param(('0:1',)),
    pytest.param(('[00:1]',)),
    pytest.param(('[0:100]',)),
    pytest.param(('[0:1] ',)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_range(*args)
