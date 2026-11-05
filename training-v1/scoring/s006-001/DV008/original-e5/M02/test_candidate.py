import copy
import pytest
from subject import edit_distance

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
    pytest.param(("", ""), 0, id="v000"),
    pytest.param(("a", "a"), 0, id="v001"),
    pytest.param(("ab", ""), 2, id="v002"),
    pytest.param(("", "ac"), 2, id="v003"),
    pytest.param(("abc", ""), 3, id="v004"),
    pytest.param(("", "xyz"), 3, id="v005"),
    pytest.param(("ab", "ac"), 1, id="v006"),
    pytest.param(("ab", "cb"), 1, id="v007"),
    pytest.param(("abc", "bc"), 1, id="v008"),
    pytest.param(("abc", "bca"), 2, id="v009"),
    pytest.param(("kitten", "sitting"), 3, id="v010"),
    pytest.param(("", "unicode"), 7, id="v011"),
    pytest.param(("日本語", ""), 3, id="v012"),
    pytest.param(("", ""), 0, id="v013"),
    pytest.param(("test", "test"), 0, id="v014"),
    pytest.param(("a", "b"), 1, id="v015"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=edit_distance(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(""), ""), id="e000"),
    pytest.param(("", StrChild("")), id="e001"),
    pytest.param((b"", ""), id="e002"),
    pytest.param(("", b""), id="e003"),
    pytest.param((1, 1), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        edit_distance(*args)
