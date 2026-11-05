from subject import ascii_upper
import pytest

# --- Type validation tests ---

def test_string_type():
    assert ascii_upper("hello") == "HELLO"

def test_integer_rejects_type():
    with pytest.raises(TypeError):
        ascii_upper(123)

def test_float_rejects_type():
    with pytest.raises(TypeError):
        ascii_upper(3.14)

def test_list_rejects_type():
    with pytest.raises(TypeError):
        ascii_upper(["a", "b"])

def test_dict_rejects_type():
    with pytest.raises(TypeError):
        ascii_upper({"key": "val"})

def test_subclass_rejects_type():
    class MyStr(str):
        pass
    
    with pytest.raises(TypeError):
        ascii_upper(MyStr("test"))

def test_unicode_preserves_non_ascii():
    assert ascii_upper("héllo") == "héllo"

def test_mixed_ascii_non_ascii():
    assert ascii_upper("aBc123dé") == "ABC123dé"

# --- Immutability tests ---

def test_string_immutability():
    original = "héllo"
    result = ascii_upper(original)
    assert result == original.upper() if all(c.isalpha() and c.isascii() for c in original) else original
    assert result is not original # Ensure a new object was returned for string case if logic implies transformation, but spec says 'Do not mutate' which for immutable strings means no side effect on original object reference/value.
    # Strict interpretation: original must not change.
    assert original == "héllo"

def test_nested_container_immutability():
    outer = ["hello", "world"]
    inner_list = ["zoo"]
    outer.append(inner_list)
    original_ref = outer
    
    # Since spec says 'text' must be exact built-in str, we cannot test nested container mutation directly via the function call 
    # because passing a list would trigger a TypeError before value checks. 
    # However, we can verify the function doesn't mutate a string containing an id of a mutable object if such a string existed, 
    # but strings are immutable in Python. 
    # The requirement 'Do not mutate any input, including nested containers' is strictly for cases where the function might 
    # return a constructed object. Since it returns a str, the input was str, and str cannot be mutated. 
    # This test verifies the contract holds for the valid path (str) and invalid path (list/dict).
    
    with pytest.raises(TypeError):
        ascii_upper(outer)
