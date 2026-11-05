from subject import edit_distance
import pytest

@pytest.mark.parametrize("left, right, expected", [
    ("", "", 0),
    ("a", "", 1),
    ("", "b", 1),
    ("abc", "", 3),
    ("", "xyz", 3),
    ("kitten", "sitting", 3),
    ("flaw", "flaw", 0),
    ("kitten", "satinn", 4),
    ("intention", "execution", 5),
    ("python", "bytecode", 5),
    ("test", "test", 0),
    ("test", "tezt", 1),
    ("test", "testt", 1),
    ("test", "ttest", 2),
    ("ABC", "abc", 4),
    ("", "123", 3),
    ("123", "321", 3),
])
def test_edit_distance_basic(left, right, expected):
    result = edit_distance(left, right)
    assert result == expected
    assert type(result) == int

@pytest.mark.parametrize("left, right", [
    ("1", 2),
    (1, 2),
    (1.5, 2.5),
    (True, False),
    (["a"], "b"),
    (("a",), "b"),
    ({"a": 1}, "b"),
    (None, "b"),
    (1 + 2j, 2 + 2j),
    (b"hello", "world"),
    ("hello".replace("h", "j"), None),
    (None, None),
    (object(), "text"),
    (range(1, 5), "text"),
    ({"key": "value"}, "dict_str"),
    (set(["a"]), "b"),
])
def test_edit_distance_rejects_invalid_types(left, right):
    with pytest.raises(TypeError):
        edit_distance(left, right)

def test_edit_distance_does_not_mutate_inputs():
    left = "cat"
    right = "dog"
    left_copy = left
    right_copy = right
    
    edit_distance(left, right)
    
    assert left == left_copy
    assert right == right_copy

def test_edit_distance_returns_exact_types():
    result = edit_distance("a", "a")
    assert type(result) is int
