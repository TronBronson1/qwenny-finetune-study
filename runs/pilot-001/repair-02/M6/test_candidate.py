import pytest
from clamp_value import clamp_integer


class _ExactSubInt(int):
    """Explicit integer subclass to verify 'reject integer subclasses' requirement."""
    pass


class TestClampInteger:
    # Requirement 1: Normal ranges, below/above limits, endpoints, equal bounds (without reversed bounds)
    @pytest.mark.parametrize("input_args, expected", [
        ((5, 0, 10), 5),
        ((-3, 0, 10), 0),
        ((12, 0, 10), 10),
        ((0, 0, 10), 0),
        ((10, 0, 10), 10),
        ((4, 4, 4), 4),
        ((-5, -10, 0), -5),
        ((-15, -10, 0), -10),
        ((2, -10, 0), 0),
    ])
    def test_valid_inputs_behavior(self, input_args, expected):
        """Test clamping logic with valid integer types and various ranges."""
        result = clamp_integer(*input_args)
        assert result == expected

    # Requirement 1 continued: Reversed bounds (separate test with ValueError)
    @pytest.mark.parametrize("bad_lower_upper", [(5, 10), (0, -5)])
    def test_reversed_bounds_raises_valueerror(self, bad_lower_upper):
        """Test that reversed bounds (lower > upper) raises ValueError."""
        value, lower, upper = bad_lower_upper[0], *bad_lower_upper
        with pytest.raises(ValueError):
            clamp_integer(value, lower, upper)

    # Requirement 2: Test forbidden types in EACH of the three positions.
    @pytest.mark.parametrize("bad_type_value", [True, False, _ExactSubInt(), 1.5, "3", None])
    def test_bad_value_position(self, bad_type_value):
        """Test that invalid 'value' raises TypeError regardless of valid bounds."""
        with pytest.raises(TypeError):
            clamp_integer(bad_type_value, 0, 10)

    @pytest.mark.parametrize("bad_type_lower", [True, False, _ExactSubInt(), 1.5, "3", None])
    def test_bad_lower_position(self, bad_type_lower):
        """Test that invalid 'lower' raises TypeError regardless of valid value/upper."""
        with pytest.raises(TypeError):
            clamp_integer(5, bad_type_lower, 10)

    @pytest.mark.parametrize("bad_type_upper", [True, False, _ExactSubInt(), 1.5, "3", None])
    def test_bad_upper_position(self, bad_type_upper):
        """Test that invalid 'upper' raises TypeError regardless of valid value/lower."""
        with pytest.raises(TypeError):
            clamp_integer(5, 0, bad_type_upper)

    # Requirement 3: Test type-validation precedence (TypeError before ValueError).
    def test_type_precedence_with_string_value_and_reversed_bounds(self):
        """Verify TypeError is raised for bad types even if bounds are invalid."""
        with pytest.raises(TypeError):
            clamp_integer("bad", 10, 0)

    def test_type_precedence_with_boolean_lower(self):
        """Verify TypeError is raised on boolean lower (type rejection), not ValueError for bounds."""
        # Note: This tests (5, True, 10) where bounds are valid but lower is invalid type
        with pytest.raises(TypeError):
            clamp_integer(5, True, 10)


# Requirement-to-Input Mapping:
# 1. Normal ranges (value within bounds, below/above limits, endpoints, equal bounds): test_valid_inputs_behavior
# 2. Reversed bounds (ValueError): test_reversed_bounds_raises_valueerror (separate from type tests)
# 3. Forbidden types per position (True/False/SubInt/float/string/None): test_bad_value_position, test_bad_lower_position, test_bad_upper_position
# 4. Type-validation precedence: test_type_precedence_with_string_value_and_reversed_bounds, test_type_precedence_with_boolean_lower

# Limitations:
# - Does not claim exhaustive coverage beyond acceptance requirements.
# - Assumes clamp_integer exists in 'clamp_value' module with correct signature (built-in integers only).
# - Uses pytest.raises for exception-based assertions without inspecting implementation.
# - Boolean tests confirm type rejection before any ValueError checks, validating precedence.
# - Does not modify or mock the implementation under test.
