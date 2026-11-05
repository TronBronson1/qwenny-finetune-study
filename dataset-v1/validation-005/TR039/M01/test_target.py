import copy
import pytest
from subject import parse_bool_word

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
    pytest.param(('true',), True, id="v000"),
    pytest.param(('false',), False, id="v001"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_bool_word(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('true'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_bool_word(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('True',), id="e004"),
    pytest.param(('false ',), id="e005"),
    pytest.param(('',), id="e006"),
    pytest.param(('1',), id="e007"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_bool_word(*args)
