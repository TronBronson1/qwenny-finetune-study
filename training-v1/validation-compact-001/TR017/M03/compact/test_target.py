import copy
import pytest
from subject import interleave_strings
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
    pytest.param(('', ''), ''),
    pytest.param(('a', ''), 'a'),
    pytest.param(('', 'b'), 'b'),
    pytest.param(('ab', '12'), 'a1b2'),
    pytest.param(('abc', '1'), 'a1bc'),
    pytest.param(('a', '123'), 'a123'),
    pytest.param(('é字', ' X'), 'é 字X'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=interleave_strings(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''), '')),
    pytest.param((b'x', '')),
    pytest.param((1, '')),
    pytest.param((None, '')),
    pytest.param(('', StrChild(''))),
    pytest.param(('', b'x')),
    pytest.param(('', 1)),
    pytest.param(('', None)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        interleave_strings(*args)
