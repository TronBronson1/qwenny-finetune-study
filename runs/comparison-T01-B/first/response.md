```python
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
    ((1, 2, 3, 4, 5), 6, (1, 2, 3, 4, 5)),
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
    ((a, b, a, b), 1, (b, a, b, a)) if False else ((1, 'x', 1, 'x'), 1, ('x', 1, 'x', 1)),
    # Nested mutable elements retain identity
    (((1,), [2]), 1, ([2], (1,))),
    (([1], (2,)), 1, ((2,), [1])),
])
def test_returns(values, steps, expected):
    result = rotate_right(values, steps)
    assert result == expected


@pytest.mark.parametrize("values,steps", [
    # Tuple subclass in values position
    ((TupleChild((1, 2)), 3), None),
    ((), TupleChild(0)),
    # Int subclass in steps position
    ((1, 2, 3), IntChild(1)),
    ((1,), IntChild(-5)),
    ((1,), IntChild(0)),
    # Boolean in values position (treated as int)
    ((True, False), -1),
    ((False,), 1),
    # Boolean in steps position
    ((1, 2, 3), True),
    ((1,), False),
])
def test_types(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    ((), "bad"),
    ((1,), 1.5),
    ((1,), None),
])
def test_type_precedence_values_invalid_first(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    ("not_tuple", 0),
    ("abc", -5),
])
def test_type_precedence_values_invalid_both(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


@pytest.mark.parametrize("values,steps", [
    ((1, 2), "bad"),
    ((), None),
])
def test_mixed_type_errors(values, steps):
    with pytest.raises(TypeError):
        rotate_right(values, steps)


Limitations: These finite cases do not cover all integer sizes, all object types, or every Unicode string combination. Nested structures beyond tuples and lists are not exercised. Oversized negative step wrapping is limited to a few examples. No performance claim follows from these tests. Type precedence with both arguments invalid is only partially explored. I have inspected these cases; this demonstration answer does not claim execution. See the separate check record for actual validation.
```
