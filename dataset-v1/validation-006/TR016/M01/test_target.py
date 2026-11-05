import copy
import pytest
from subject import count_vowels

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
    pytest.param(('',), 0, id="v000"),
    pytest.param(('AEIOUaeiou',), 10, id="v001"),
    pytest.param(('rhythm',), 0, id="v002"),
    pytest.param(('Apple pie',), 4, id="v003"),
    pytest.param(('éÁy',), 0, id="v004"),
    pytest.param(('a1 E!',), 2, id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=count_vowels(*args)
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
        count_vowels(*args)
