from subject import edit_distance
import pytest

# --- Type validation tests ---

def test_edit_distance_both_valid_strings():
    assert edit_distance("kitten", "sitting") == 3

def test_edit_distance_empty_vs_single():
    assert edit_distance("", "a") == 1

def test_edit_distance_equal_strings():
    assert edit_distance("abc", "abc") == 0

def test_edit_distance_one_empty():
    assert edit_distance("test", "") == 4

# --- ValueError / Invalid Type tests ---

def test_edit_distance_left_not_string():
    with pytest.raises(TypeError):
        edit_distance(123, "right")

def test_edit_distance_left_subclass_string():
    class MyStr(str):
        pass
    
    with pytest.raises(TypeError):
        edit_distance(MyStr("left"), "right")

def test_edit_distance_right_not_string():
    with pytest.raises(TypeError):
        edit_distance("left", 456)

def test_edit_distance_right_subclass_string():
    class MyStr(str):
        pass
    
    with pytest.raises(TypeError):
        edit_distance("left", MyStr("right"))

# --- Unicode and Case-sensitivity tests ---

def test_edit_distance_unicode_chars():
    # Test 'cherry' vs 'cherry' (same) -> 0
    assert edit_distance("cherry", "cherry") == 0
    # Test 'cherry' vs 'cherry' (different case) -> 1 ('y' vs 'Y')
    assert edit_distance("Cherry", "cherry") == 1

def test_edit_distance_mixed_unicode():
    assert edit_distance("café", "café") == 0
    assert edit_distance("café", "Café") == 1

# --- Explicit value checks (no parameterized expansion) ---

def test_edit_distance_specific_values():
    assert edit_distance("cat", "cut") == 1
    assert edit_distance("cat", "bat") == 1
    assert edit_distance("cat", "dog") == 3
    assert edit_distance("horse", "ros") == 3
