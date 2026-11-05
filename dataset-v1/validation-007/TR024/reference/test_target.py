import copy
import pytest
from subject import ascii_upper

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
    pytest.param(('',), '', id="v000"),
    pytest.param(('abcXYZ',), 'ABCXYZ', id="v001"),
    pytest.param(('z-a 9',), 'Z-A 9', id="v002"),
    pytest.param(('éßı',), 'éßı', id="v003"),
    pytest.param(('a\nb',), 'A\nB', id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=ascii_upper(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        ascii_upper(*args)
