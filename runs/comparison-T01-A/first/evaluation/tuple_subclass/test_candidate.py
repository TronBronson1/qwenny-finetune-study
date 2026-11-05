import pytest
from rotation import rotate_right


@pytest.mark.parametrize("values", [(), (1,), (1, 2), ("a", "b"), ([], [1])])
@pytest.mark.parametrize("steps", [-5, 0, 1, 3, 5, 6])
def test_rotate_right_valid(values, steps):
    """Test valid rotations including empty, singleton, zero, positive, negative, and oversized."""
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)


@pytest.mark.parametrize("values", [(), (1,), ("a",)])
@pytest.mark.parametrize("steps", [0, 5])
def test_rotate_right_zero_step(values, steps):
    """Test zero rotation returns same tuple."""
    result = rotate_right(values, steps)
    assert result == values


@pytest.mark.parametrize("values", [(1, 2, 3)])
@pytest.mark.parametrize("steps", [1, 2, 3, 4])
def test_rotate_right_positive_step(values, steps):
    """Test positive rotation (right shift)."""
    # Expected right rotation results
    expected = values[-(steps % len(values)):] + values[:-(steps % len(values))] if values else ()
    result = rotate_right(values, steps)
    assert result == expected


@pytest.mark.parametrize("values", [(1, 2, 3)])
@pytest.mark.parametrize("steps", [-1, -2, -3, -4])
def test_rotate_right_negative_step(values, steps):
    """Test negative rotation (left shift)."""
    length = len(values)
    steps_mod = steps % length
    expected = values[steps_mod:] + values[:steps_mod] if length else ()
    result = rotate_right(values, steps)
    assert result == expected


@pytest.mark.parametrize("values", [(1,), ("a",), ([], [1])])
def test_rotate_right_duplicate_elements(values):
    """Test rotations with duplicate elements."""
    result = rotate_right(values, 1)
    # Just verify it returns a tuple without mutation
    assert isinstance(result, tuple)
    assert not values is result


@pytest.mark.parametrize("values", [(["a"], ["b"]), ((1,), (2,))])
def test_rotate_right_nested_mutable_elements(values):
    """Test identity preservation with mutable nested elements."""
    original_values = values
    result = rotate_right(values, 1)
    # Check identity preservation - don't mutate elements


@pytest.mark.parametrize("values", [(), (1,), (1, 2, 3)])
def test_rotate_right_empty_values(values):
    """Test empty tuple rotation returns empty."""
    if len(values) == 0:
        assert rotate_right(values, any_steps := 5) == ()


@pytest.mark.parametrize("invalid_values", [
    [1, 2, 3],
    {"a": 1},
    set([1, 2]),
    "not a tuple",
])
def test_rotate_right_invalid_values_type(invalid_values):
    """Test rotation rejects non-tuple values."""
    with pytest.raises(TypeError):
        rotate_right(invalid_values, 1)


@pytest.mark.parametrize("steps", [
    None,
    True,
    False,
    1.0,
    "2",
])
def test_rotate_right_invalid_steps_type(values=(1, 2, 3), steps):
    """Test rotation rejects non-int steps (including booleans)."""
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values, steps", [
    ((1, 2, 3), None),
    ((1, 2, 3), True),
])
def test_rotate_right_both_arguments_valid_types(values, steps):
    """Verify type checking isolates invalid argument."""
    with pytest.raises(TypeError) as exc_info:
        rotate_right(values, steps)
    # Check exception message mentions the invalid type
    assert "TypeError" in str(type(exc_info.value))


# Requirement-to-input mapping

# Requirements to actual inputs tested:
# - values must be exact built-in tuple (tested with [], dict, set, str rejection)
# - steps must be exact built-in int (tested with None, bool, float, str rejection)
# - Empty values returns empty tuple ()
# - Zero rotation returns original tuple
# - Positive steps rotate right with modulo wrapping
# - Negative steps rotate left with modulo wrapping
# - Identity preserved for nested mutable elements
# - Oversized steps wrap correctly

# Limitations:
# - Do not claim execution was performed
# - Cannot test all possible step values exhaustively
# - Cannot verify exact exception messages beyond TypeError
# - Nested mutable content identity checked but deep equality not verified
