# test_rotate.py
import pytest
from subject import rotate_right


class SubTuple(tuple):
    pass


class FakeInt(int):
    pass


class FakeIntSubclass(int):
    pass


@pytest.mark.parametrize(
    ['values', 'steps'],
    [
        ([1], 1),
        ([1, 2], 1),
        ([1, 2, 3], 0),
        ([1, 2, 3], 1),
        ([1, 2, 3], 2),
        ([1, 2, 3], 3),
        ([1, 2, 3], 4),
        ([1, 2, 3], -1),
        ([1, 2, 3], -2),
        ([1, 2, 3], -3),
        ([1, 2, 3], -4),
        ([1, 2, 3], 6),
        ([1, 2, 3], -6),
        ([], 0),
        ([], 1),
        ([1], 0),
        ([1], 1),
    ],
)
def test_rotate_right_valid(values, steps):
    """
    Ordinary return-value cases.
    Verifies valid tuple and valid int inputs return correctly rotated results.
    """
    result = rotate_right(values, steps)
    
    # Calculate expected result based on rotation logic
    expected = rotate_right(values, 0) # Identity
    n = len(values)
    if n == 0:
        expected = ()
    else:
        # Right rotate: index i moves to (i + steps) % n
        # Effectively: result[i] = values[(i - steps) % n]
        # Python slice logic equivalent to this
        # Slicing: result = values[-steps:] + values[:-steps]
        # Handle negative steps correctly for slices
        if steps < 0:
            shift = steps % n
            expected = values[:shift] + values[shift:]
        else:
            shift = steps % n
            expected = values[-shift:] + values[:-shift] if shift != 0 else values
    
    assert result == expected


@pytest.mark.parametrize(
    ['values', 'steps'],
    [
        (SubTuple([1]), 1),
        ((1, 2), SubTuple([1])),
        ([1, 2], 1),
        ((1, 2), 'float'),
        ([], True),
        ([], False),
        ([], FakeInt(1)),
        ([], FakeIntSubclass(1)),
    ],
)
def test_rotate_right_invalid_input_type(values, steps):
    """
    Expected-exception cases.
    Verifies TypeError is raised before value/shape checks for invalid types.
    Isolates invalid input by holding other arguments valid where possible.
    """
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize(
    ['values', 'steps'],
    [
        ([1, 2], 1),
        ([1, 2], 3),
        ([1, 2], -1),
        ([1, 2], -2),
        ([], 1),
        ([], 2),
        ([], -1),
    ],
)
def test_rotate_right_no_mutation(values, steps):
    """
    Verifies no input mutation, including nested containers.
    Input identity should be preserved in output.
    """
    result = rotate_right(values, steps)
    
    assert values is not result
    for v_val, r_val in zip(values, result):
        assert v_val is r_val
