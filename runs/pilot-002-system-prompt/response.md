```python
import pytest
from clamp_value import clamp_integer


class TestClampIntegerNormalRanges:
    """Test normal clamping behavior with valid integer inputs."""

    def test_value_within_bounds_positive(self):
        assert clamp_integer(5, 0, 10) == 5

    def test_value_below_lower_bound(self):
        assert clamp_integer(-3, 0, 10) == 0

    def test_value_above_upper_bound(self):
        assert clamp_integer(12, 0, 10) == 10

    def test_negative_bounds_positive_value(self):
        assert clamp_integer(4, -10, 0) == 0

    def test_negative_range_both_args_negative(self):
        assert clamp_integer(-5, -10, -3) == -5

    def test_equal_lower_and_upper(self):
        assert clamp_integer(4, 4, 4) == 4


class TestClampIntegerInvalidTypesValuePosition:
    """Test type validation when 'value' argument is invalid."""

    def test_true_as_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(True, 0, 10))

    def test_false_as_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(False, 0, 10))

    def test_float_as_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(1.5, 0, 10))

    def test_string_as_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer("3", 0, 10))

    def test_none_as_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(None, 0, 10))


class TestClampIntegerInvalidTypesLowerPosition:
    """Test type validation when 'lower' argument is invalid."""

    def test_true_as_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, True, 10))

    def test_false_as_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, False, 10))

    def test_float_as_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 1.5, 10))

    def test_string_as_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, "0", 10))

    def test_none_as_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, None, 10))


class TestClampIntegerInvalidTypesUpperPosition:
    """Test type validation when 'upper' argument is invalid."""

    def test_true_as_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, True))

    def test_false_as_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, False))

    def test_float_as_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, 1.5))

    def test_string_as_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, "10"))

    def test_none_as_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, None))


class TestClampIntegerIntSubclassInvalid:
    """Test that integer subclasses are rejected."""

    class MyInt(int):
        pass

    def test_subclass_value_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(MyInt(5), 0, 10))

    def test_subclass_lower_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, MyInt(0), 10))

    def test_subclass_upper_raises_type_error(self):
        pytest.raises(TypeError, lambda: clamp_integer(5, 0, MyInt(10)))


class TestClampIntegerReversedBounds:
    """Test ValueError when lower > upper."""

    def test_lower_greater_than_upper_raises_value_error(self):
        with pytest.raises(ValueError):
            clamp_integer(5, 10, 0)


class TestClampIntegerTypeValidationPrecedence:
    """Ensure type validation occurs before range checking."""

    def test_string_value_precedence_over_reversed_bounds(self):
        # Should raise TypeError for invalid value type, not ValueError for bounds
        with pytest.raises(TypeError):
            clamp_integer("bad", 10, 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Requirement-to-Input Mapping Summary
| Requirement | Input Cases Covered |
|-------------|---------------------|
| Normal ranges (positive/negative) | `TestClampIntegerNormalRanges` |
| Below/above limits | `clamp_integer(-3, 0, 10)` / `clamp_integer(12, 0, 10)` |
| Exact endpoints | `clamp_integer(4, 4, 4)` |
| Equal bounds | Same as exact endpoints test |
| Reversed bounds | `clamp_integer(5, 10, 0)` |
| Invalid value (True/False/float/str/None) | 5 cases in `TestClampIntegerInvalidTypesValuePosition` |
| Invalid lower (True/False/float/str/None) | 5 cases in `TestClampIntegerInvalidTypesLowerPosition` |
| Invalid upper (True/False/float/str/None) | 5 cases in `TestClampIntegerInvalidTypesUpperPosition` |
| Integer subclass rejection | 3 cases in `TestClampIntegerIntSubclassInvalid` |
| Type-validation precedence | 1 case in `TestClampIntegerTypeValidationPrecedence` |

## Limitations
- Tests were not executed; this is a specification only.
- Boolean types are rejected even though they subclass `int`.
- Integer subclasses (non-builtin) are rejected per contract.
- Not exhaustive beyond specified cases; other edge cases (e.g., large integers) untested.
- No fixtures used; all tests are standalone.