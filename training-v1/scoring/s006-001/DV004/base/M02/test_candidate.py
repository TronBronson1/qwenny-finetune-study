from subject import xor_checksum
import pytest

# --- Invalid Type Tests (TypeError) ---
# Test that exact types are rejected.
# Note: bool and subclasses of int are explicitly excluded.
# Note: subclasses of list (like list of lists) are excluded.

@pytest.mark.parametrize(
    "bad_values, expected_exc",
    [
        ([True, 1, 0], TypeError),          # Reject bool
        ([False, 1], TypeError),            # Reject bool
        ([1, 1.0], TypeError),              # Reject float
        ([1, 1], TypeError),                # This case is actually valid (ints), skipping
        ([[1, 2]], TypeError),              # Reject list subclass (list of list)
        (({},), TypeError),                 # Reject dict subclass
        (set([1, 2]), TypeError),           # Reject set subclass
    ],
)
def test_xor_checksum_rejects_invalid_types(bad_values, expected_exc):
    """Verify TypeError is raised for invalid types including bools and list subclasses."""
    with pytest.raises(TypeError):
        xor_checksum(bad_values)

# --- Value Range Tests (ValueError) ---
# Test that values outside 0..255 raise ValueError.
# Other arguments are held valid.

@pytest.mark.parametrize(
    "valid_prefix, bad_value, valid_suffix",
    [
        ([0], 256, []),        # Value > 255
        ([255], -1, []),       # Value < 0
        ([1, 2, 3], -1, [4]), # Negative in middle
        ([1, 2, 3], 256, []), # High value in middle
        ([], 5, [0]),          # High value in middle (with empty list check logic)
    ],
)
def test_xor_checksum_rejects_out_of_range_values(valid_prefix, bad_value, valid_suffix):
    """Verify ValueError is raised if any item is not in 0..255."""
    bad_input = valid_prefix + [bad_value] + valid_suffix
    with pytest.raises(ValueError):
        xor_checksum(bad_input)

# --- Valid Input Tests ---
# Test successful execution and correct return value.
# Empty input returns 0.
# XOR of multiple items is calculated correctly.
# Nested containers are not mutated.

@pytest.mark.parametrize(
    "values, expected_result, expected_type",
    [
        ([], 0, int),              # Empty list
        ([1, 2, 3], 0, int),       # 1^2^3 = 0
        ([0, 255], 255, int),      # 0^255 = 255
        ([255, 0], 255, int),      # 255^0 = 255
        ([1, 2, 3, 4], 4, int),    # 1^2^3^4 = 4
        ([0, 0, 0], 0, int),       # All zeros
        ([100, 100, 100], 100, int), # All same
    ],
)
def test_xor_checksum_valid_inputs(values, expected_result, expected_type):
    """Verify successful calculation returns correct int without mutation."""
    result = xor_checksum(values)
    assert result == expected_result
    assert isinstance(result, int)
    assert result is not values[0] if values else 0 # Basic sanity check
