import pytest
from prefix_tools import strip_prefix

class IntChild(int):
    pass

class StrChild(str):
    pass

@pytest.mark.parametrize("left,right,expected", [("abc", "a", "bc"), ("abc", "abc", ""), ("abc", "z", "abc"), ("", "a", ""), ("aaaa", "a", "aaa"), ("Abc", "a", "Abc"), ("ba", "a", "ba"), (" ab", " ", "ab"), ("éclair", "é", "clair"), ("abc", "abcd", "abc")])
def test_returns(left, right, expected):
    assert strip_prefix(left, right) == expected

@pytest.mark.parametrize("left,right", [(True, "a"), (1, "a"), (None, "a"), (b"a", "a"), (StrChild("a"), "a"), ("abc", True), ("abc", 1), ("abc", None), ("abc", b"a"), ("abc", StrChild("a"))])
def test_types(left, right):
    with pytest.raises(TypeError):
        strip_prefix(left, right)

@pytest.mark.parametrize("left,right", [("abc", ""), ("", "")])
def test_values(left, right):
    with pytest.raises(ValueError):
        strip_prefix(left, right)

@pytest.mark.parametrize("left,right", [(None, "")])
def test_type_precedence(left, right):
    with pytest.raises(TypeError):
        strip_prefix(left, right)
