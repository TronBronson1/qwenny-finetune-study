from subject import xor_checksum
import pytest

# --- Invalid Type Tests (TypeError) ---
# Test that exact types are rejected.
# Note: bool and subclasses of int are explicitly excluded.
# Note: subclasses of list (like list of lists) are explicitly excluded.

# Case 1: Single value is a boolean (subclass of int)
def test_bool_rejected():
    with pytest.raises(TypeError):
        xor_checksum([True, False])

# Case 2: Single value is a subclass of int
class MyInt(int):
    pass

def test_int_subclass_rejected():
    with pytest.raises(TypeError):
        xor_checksum([MyInt(5)])

# Case 3: Single value is a subclass of list (tuple, list of lists, etc.)
class MyList(list):
    pass

def test_list_subclass_rejected():
    with pytest.raises(TypeError):
        xor_checksum([1, MyList([2, 3])])

# --- Valid Value/Shape Tests (Correct return value) ---
# Verify exact types of inputs and outputs, and XOR logic.

# Case 1: Empty list returns 0
def test_empty_returns_zero():
    assert xor_checksum([]) == 0

# Case 2: Single byte (0..255) returns that byte
def test_single_byte_returns_value():
    assert xor_checksum([65]) == 65

# Case 3: Standard XOR of two distinct bytes
def test_xor_two_bytes():
    assert xor_checksum([1, 2]) == 3
    assert xor_checksum([2, 1]) == 3

# Case 4: XOR of three bytes
def test_xor_three_bytes():
    assert xor_checksum([1, 2, 3]) == 0  # 1^2^3 = 0

# Case 5: Values containing 0 (identity element)
def test_xor_with_zero():
    assert xor_checksum([0, 1, 2]) == 3

# Case 6: All identical values (result is 0 if odd count, val if even count)
def test_identical_values_even_count():
    assert xor_checksum([5, 5, 5, 5]) == 5

def test_identical_values_odd_count():
    assert xor_checksum([5, 5, 5]) == 5

# Case 7: Maximum valid byte value (255)
def test_max_byte():
    assert xor_checksum([255]) == 255

# Case 8: Mixed valid bytes
def test_mixed_bytes():
    assert xor_checksum([255, 100, 200]) == 55  # 255 ^ 100 = 155; 155 ^ 200 = 55
    assert xor_checksum([1, 2, 3, 4]) == 4     # 1^2^3 = 0; 0^4 = 4

# Case 9: Ensure non-mutating behavior for input list
def test_input_not_mutated():
    original = [10, 20, 30]
    result = xor_checksum(original)
    assert original == [10, 20, 30]
    assert result == 0  # 10^20^30 = 0

# Case 10: Ensure exact types for output (int)
def test_output_is_int():
    output = xor_checksum([1, 2])
    assert isinstance(output, int)
    assert not isinstance(output, bool)

# --- Invalid Value Tests (ValueError) ---
# Verify that non-byte values (outside 0..255) or invalid shapes raise ValueError.
# Input is a list, but the *values inside* are invalid.

# Case 1: Value < 0
def test_value_negative_raises():
    with pytest.raises(ValueError):
        xor_checksum([-1])

# Case 2: Value > 255
def test_value_greater_than_255_raises():
    with pytest.raises(ValueError):
        xor_checksum([256])

# Case 3: Value > 255 in list context
def test_value_greater_than_255_in_list_raises():
    with pytest.raises(ValueError):
        xor_checksum([0, 256])

# Case 4: List contains a float (even if value is in range)
def test_float_value_raises():
    with pytest.raises(ValueError):
        xor_checksum([0.5])

# Case 5: List contains a string
def test_string_value_raises():
    with pytest.raises(ValueError):
        xor_checksum(["a"])

# Case 6: List contains None
def test_none_value_raises():
    with pytest.raises(ValueError):
        xor_checksum([None])

# Case 7: List contains a nested list (list subclass rejection covered above, 
# but here we isolate the list subclass as an element within a valid top-level list)
class MyList(list):
    pass

def test_nested_list_element_raises():
    with pytest.raises(ValueError):
        xor_checksum([1, MyList([2])])

# Case 8: List contains a subclass of int with value > 255
class MyInt(int):
    pass

def test_int_subclass_large_value_raises():
    with pytest.raises(ValueError):
        xor_checksum([MyInt(256)])

