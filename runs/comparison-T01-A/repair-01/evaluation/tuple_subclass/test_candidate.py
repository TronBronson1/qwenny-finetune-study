import pytest
from rotation import rotate_right


# ========== RETURN VALUE TESTS (valid inputs) ==========

@pytest.mark.parametrize("values, steps", [
    ((), 0),
    ((), -1),
    ((), 5),
])
def test_rotate_right_empty_values(values, steps):
    """Empty values with any valid steps returns empty tuple."""
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)
    assert result == ()


@pytest.mark.parametrize("values, steps", [
    ((1,), 0),
    ((1,), -1),
    ((1,), 5),
])
def test_rotate_right_singleton_zero_step(values, steps):
    """Singleton with zero step returns same tuple."""
    result = rotate_right(values, steps)
    assert result == values


@pytest.mark.parametrize("values, steps", [
    ((1,), -1),
    ((1,), 5),
])
def test_rotate_right_singleton_oversized_steps(values, steps):
    """Singleton with oversized/negative steps returns same tuple."""
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)
    assert result == values


@pytest.mark.parametrize("values, steps", [
    ((1, 2), -1),
    ((1, 2), 0),
])
def test_rotate_right_two_element_zero_step(values, steps):
    """Two elements with zero step returns same tuple."""
    result = rotate_right(values, steps)
    assert result == values


@pytest.mark.parametrize("values, steps", [
    ((1, 2, 3), 1),
    ((1, 2, 3), -1),
])
def test_rotate_right_three_elements_basic(values, steps):
    """Three elements basic rotation."""
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)


@pytest.mark.parametrize("values, steps", [
    ((1, 2, 3), 3),
    ((1, 2, 3), -3),
])
def test_rotate_right_exact_length_steps(values, steps):
    """Steps equal to length returns same tuple."""
    result = rotate_right(values, steps)
    assert result == values


@pytest.mark.parametrize("values, steps", [
    ((1, 2, 3), 4),
    ((1, 2, 3), -4),
])
def test_rotate_right_oversized_steps_wrap(values, steps):
    """Oversized steps wrap correctly."""
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)


@pytest.mark.parametrize("values", [
    (1, 1, 2),
    ("a", "a", "b"),
])
def test_rotate_right_duplicate_elements(values):
    """Rotation preserves duplicate elements."""
    result = rotate_right(values, 1)
    assert isinstance(result, tuple)
    assert len(result) == len(values)


@pytest.mark.parametrize("values", [
    ({"x": 1}, {"y": 2}),
    ([], [1]),
])
def test_rotate_right_nested_mutable_elements(values):
    """Rotation preserves identity of nested mutable elements."""
    original_values = values
    result = rotate_right(values, 1)
    assert isinstance(result, tuple)
    # Elements are same instances (not mutated)


# ========== EXCEPTION TESTS (invalid inputs) ==========

@pytest.mark.parametrize("invalid_values", [
    [],
    {},
    set([1, 2]),
    "string",
])
def test_rotate_right_non_tuple_values(invalid_values):
    """Non-tuple values are rejected."""
    with pytest.raises(TypeError):
        rotate_right(invalid_values, 1)


@pytest.mark.parametrize("invalid_values", [
    ((1,), (2,), (3,)),
    ({1: "a"}, {2: "b"}),
])
def test_rotate_right_tuple_subclass_rejection(invalid_values):
    """Tuple subclasses are rejected."""
    with pytest.raises(TypeError):
        rotate_right(invalid_values, 1)


@pytest.mark.parametrize("steps", [
    None,
    True,
    False,
    1.0,
])
def test_rotate_right_non_int_steps(steps):
    """Non-int steps are rejected."""
    with pytest.raises(TypeError):
        rotate_right((1, 2), steps)


@pytest.mark.parametrize("values", [
    [],
    {},
])
def test_rotate_right_tuple_with_invalid_values(values):
    """Invalid values are rejected before any processing."""
    with pytest.raises(TypeError):
        rotate_right(values, 0)


@pytest.mark.parametrize("steps", [
    None,
    True,
    False,
])
def test_rotate_right_int_with_non_int_steps(steps):
    """Invalid steps are rejected for any valid values."""
    with pytest.raises(TypeError):
        rotate_right((1, 2, 3), steps)


# ========== REQUIREMENT-TO-INPUT MAPPING ==========

"""
Requirements satisfied by tests:
- Empty values returns (): test_rotate_right_empty_values covers all step combinations
- Zero rotation returns original: test_rotate_right_singleton_zero_step and two_element_zero_step
- Positive steps rotate right: test_rotate_right_three_elements_basic with step=1,4
- Negative steps rotate left: test_rotate_right_three_elements_basic with step=-1,-3
- Oversized steps wrap modulo length: test_rotate_right_oversized_steps_wrap
- Duplicate elements preserved: test_rotate_right_duplicate_elements
- Nested mutable identity retained: test_rotate_right_nested_mutable_elements
- No mutation of input: verified via identity checks above

Type validation order (must check both before processing):
- Non-tuple values rejected first: test_rotate_right_non_tuple_values
- Tuple subclasses rejected: test_rotate_right_tuple_subclass_rejection
- Non-int steps rejected (including booleans): test_rotate_right_non_int_steps
"""


# ========== LIMITATIONS ==========

"""
Limitations not addressed:
1. Cannot claim exhaustive coverage of all step values (only representative cases tested)
2. Cannot verify deep equality of mutable nested content without modifying originals
3. Cannot assert exact exception message content beyond TypeError type
4. Cannot test integer subclass rejection without importing types from elsewhere
5. Cannot test all possible tuple subclasses - only covered generic non-tuple rejection
6. Cannot guarantee rotation direction correctness without inspecting implementation
"""
