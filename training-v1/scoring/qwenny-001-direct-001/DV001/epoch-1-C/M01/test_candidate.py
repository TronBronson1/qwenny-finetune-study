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
