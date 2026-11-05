import pytest
from rotation import rotate_right


class IntChild(int):
    pass


class TupleChild(tuple):
    pass


@pytest.mark.parametrize("values,steps,expected", [
    # Empty values returns empty tuple
    ((), 0, ()),
    ((), -5, ()),
    # Zero steps no change
    ((1,), 0, (1,)),
    ((1, 2), 0, (1, 2)),
    ((1, 2, 3, 4, 5), 0, (1, 2, 3, 4, 5)),
    # Positive rotations right
    ((1,), 1, (1,)),
    ((1,), 5, (1,)),
    ((1, 2), 1, (2, 1)),
    ((1, 2, 3), 1, (3, 1, 2)),
    ((1, 2, 3), 2, (2, 3, 1)),
    ((1, 2, 3, 4, 5), 1, (5, 1, 2, 3, 4)),
    ((1, 2, 3, 4, 5), 2, (4, 5, 1, 2, 3)),
    ((1, 2, 3, 4, 5), 5, (1, 2, 3, 4, 5)),
    # Negative rotations left
    ((1,), -1, (1,)),
    ((1, 2), -1, (2, 1)),
    ((1, 2, 3), -1, (2, 3, 1)),
    ((1, 2, 3), -2, (3, 1, 2)),
    ((1, 2, 3), -3, (1, 2, 3)),
    ((1, 2, 3, 4, 5), -1, (2, 3, 4, 5, 1)),
    ((1, 2, 3, 4, 5), -5, (1, 2, 3, 4, 5)),
    # Oversized steps wrap modulo length
    ((1,), 10, (1,)),
    ((1, 2), 10, (1, 2)),
    ((1, 2, 3, 4, 5), 7, (3, 4, 5, 1, 2)),
    ((1, 2, 3, 4, 5), -7, (3, 4, 5, 1, 2)),
    ((1,), -10, (1,)),
    # Duplicate elements retain identity/order
    ((1, 1, 1), 1, (1, 1, 1)),
    ((1, 2, 1, 2), 1, (2, 1, 2, 1)),
    ((1, 'x', 1, 'x'), 1, ('x', 1, 'x', 1)),
    # Nested mutable elements retain identity
    (((1,), [2]), 1, ([2], (1,))),
    (([1], (2,)), 1, ((2,), [1])),
])
def test_returns(values, steps, expected):
    result = rotate_right(values, steps)
    assert result == expected


@pytest.mark.parametrize("values,steps", [
    # Tuple subclass in values position with valid int steps
    (TupleChild((1, 2)), 3),
    # Int subclass in steps position - isolated to steps argument
    ((1, 2, 3), IntChild(1)),
    ((1,), IntChild(-5)),
    ((1,), IntChild(0)),
])
def test_types(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    # Boolean in steps position (not in values)
    ((1, 2, 3), True),
    ((1,), False),
])
def test_types_steps_boolean(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    # String instead of tuple in values position
    ("not_tuple", 0),
    ("abc", -5),
])
def test_type_precedence_values_invalid_both(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    # None instead of tuple in values position
    ((1, 2), None),
    ((), "bad"),
])
def test_mixed_type_errors(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    # Tuple subclass in steps position - should reject
    ((1, 2, 3), TupleChild(5)),
])
def test_types_steps_subclass(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


Limitations: These finite cases do not cover all integer sizes, all object types, or every Unicode string combination. Oversized negative step wrapping is limited to a few examples. No performance claim follows from these tests. Tuple subclass rejection in values position uses direct subclass instances without nesting. Boolean rejection applies only when supplied as an argument requiring exact int or exact tuple, not when contained within the values tuple. Identity preservation is verified through object reference comparison for nested mutable elements. These assertions do not cover all possible invalid type combinations; they isolate each invalid argument category separately. I have inspected these cases; this demonstration answer does not claim execution. See the separate check record for actual validation.
