import pytest
from subject import path_segments

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), [], id="v000"),
    pytest.param(('/',), [], id="v001"),
    pytest.param(('//a///b/',), ['a', 'b'], id="v002"),
    pytest.param(('/./../',), ['.', '..'], id="v003"),
    pytest.param(('a\\b/c',), ['a\\b', 'c'], id="v004"),
    pytest.param(('/ a /字/',), [' a ', '字'], id="v005"),
])
def test_values(args,expected):
    actual=path_segments(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        path_segments(*args)
