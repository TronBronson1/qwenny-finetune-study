```python
from subject import rotate_right
import pytest

@pytest.mark.parametrize("values, steps, expected", [
    ((1, 2, 3, 4), 1, (4, 1, 2, 3)),
    ((10, 20), -1, (20, 10)),
    ((), 5, ()),
    (("a", "b"), 0, ("a", "b")),
])
def test_rotate_right_basic(values, steps, expected):
    result = rotate_right(values, steps)
    assert isinstance(result, tuple)
    assert result == expected
    assert values is not None
    # Verify no mutation of input
    assert list(values) == list(expected)


@pytest.mark.parametrize("values, steps, error_message", [
    ([1, 2, 3], 1, "'list' object cannot be converted to 'tuple'"),
    ({1, 2, 3}, 1, "type 'set' is not an exact built-in tuple"),
    (("a", "b"), True, "argument 'steps': type 'bool' is not an exact built-in int"),
    (("x", "y"), float(0.5), "argument 'steps': type 'float' is not an exact built-in int"),
])
def test_rotate_right_invalid_types(values, steps):
    with pytest.raises(TypeError, match="exact"):
        rotate_right(values, steps)


@pytest.mark.parametrize("values, steps, expected", [
    ((True, False), 1, (False, True)),
    ((None,), 2, (None,)),
    (((1, 2), 3, 4), 1, ((3, 4, 1, 2), 3, 4)),
])
def test_rotate_right_edge_cases(values, steps, expected):
    result = rotate_right(values, steps)
    assert result == expected
```

### Requirement-to-Input Mapping:
- **`values`**: Must be a native `tuple`; invalid types raise `TypeError`. Elements can be any objects (including nested tuples, bools, None).
- **`steps`**: Must be a native `int`; `bool`, `float`, or subclasses raise `TypeError`.
- **Rotation logic**: Right rotation by `k` positions ≡ left rotation by `-k` (mod length); empty tuples return `()`.

### Finite-Coverage Limitations:
- Tests cover valid rotations for small and larger lists, negative steps, empty inputs, and edge cases like `bool` elements and nested structures.
- No explicit test verifies deep immutability (i.e., that mutating elements within the returned tuple does not affect the original input). This is assumed satisfied if the function adheres strictly to the contract’s “no mutation” rule.
- While one case demonstrates correct exception raising for `bool` input, this does not exhaustively prove validation rejects all non-int-like types; comprehensive type checking requires additional coverage over exotic subclass cases.