from subject import rotate_right
import pytest

# Test cases for valid inputs
@pytest.mark.parametrize("values, steps, expected", [
    # Empty tuple
    ((), 0, ()),
    # Single element
    ((1,), 1, (1,)),
    # Two elements
    ((1, 2), 1, (2, 1)),
    # Three elements
    ((1, 2, 3), 1, (3, 1, 2)),
    # Negative steps (rotate left)
    ((1, 2, 3), -1, (2, 3, 1)),
    # Wrap around
    ((1, 2, 3), 4, (3, 1, 2)),
    # Wrap around negative
    ((1, 2, 3), -2, (3, 1, 2)),
    # Large steps
    ((1, 2, 3), 100, (3, 1, 2)),
])
def test_rotate_right_valid(values, steps, expected):
    result = rotate_right(values, steps)
    assert result == expected
    assert isinstance(result, tuple)
    assert type(result) is tuple

# Test cases for invalid inputs
@pytest.mark.parametrize("values, steps", [
    # List instead of tuple
    ([1, 2, 3], 1),
    # Tuple subclass
    (tuple([1, 2, 3]), 1),
    # Bool instead of int
    ((1, 2, 3), True),
    # Bool subclass (if applicable, though bool is subclass of int)
    ((1, 2, 3), False),
    # Float instead of int
    ((1, 2, 3), 1.5),
    # None instead of int
    ((1, 2, 3), None),
])
def test_rotate_right_invalid_types(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)
