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
    pytest.param(('a',), 'A', id="v001"),
    pytest.param(('abc',), 'ABC', id="v002"),
    pytest.param(('ABC',), 'ABC', id="v003"),
    pytest.param(('Aa1!',), 'Aa1!', id="v004"),
    pytest.param(('αβγ',), 'αβγ', id="v005"),
    pytest.param(('123',), '123', id="v006"),
    pytest.param(('',), '', id="v007"),
    pytest.param(('  ',), '  ', id="v008"),
    pytest.param(('🔍',), '🔍', id="v009"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=ascii_upper(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('x'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild('x'),), id="e004"),
    pytest.param((StrChild('x'),), id="e005"),
    pytest.param((b'x',), id="e006"),
    pytest.param((1,), id="e007"),
    pytest.param((None,), id="e008"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        ascii_upper(*args)
