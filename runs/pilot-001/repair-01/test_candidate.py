import pytest
from clamp_value import clamp_integer


class _ExactSubInt(int):
    """Explicit integer subclass to verify 'reject integer subclasses' requirement."""
    pass


class TestClampInteger:
    # Requirement 1: Normal ranges, below/above limits, endpoints, equal bounds, reversed bounds.
    @pytest.mark.parametrize("input_args, expected", [
        # Value within bounds (normal)
        ((5, 0, 10), 5),
        # Below lower bound -> clamp to lower
        ((-3, 0, 10), 0),
        # Above upper bound -> clamp to upper
        ((12, 0, 10), 10),
        # Exact endpoint lower
        ((0, 0, 10), 0),
        # Exact endpoint upper
        ((10, 0, 10), 10),
        # Equal bounds (single point)
        ((4, 4, 4), 4),
        # Negative ranges (value inside)
        ((-5, -10, 0), -5),
        # Negative ranges (clamp to lower)
        ((-15, -10, 0), -10),
        # Negative ranges (clamp to upper)
        ((2, -10, 0), 0),
        # Reversed bounds (ValueError expected)
        ((5, 10, 0), pytest.raises(ValueError)),
    ])
    def test_valid_inputs_behavior(self, input_args, expected):
        """Test clamping logic with valid integer types and various ranges."""
        if isinstance(expected, type):  # Handle pytest.raises wrapper
            with expected:
                clamp_integer(*input_args)
        else:
            result = clamp_integer(*input_args)
            assert result == expected

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

    def test_type_precedence_with_boolean_lower_and_reversed_bounds(self):
        """Verify TypeError is raised on boolean lower before checking ValueError."""
        with pytest.raises(TypeError):
            clamp_integer(5, True, 10)


# Requirement-to-Input Mapping:
# 1. Normal/negative ranges: test_valid_inputs_behavior (value within bounds, below/above limits, endpoints, equal bounds, reversed bounds)
# 2. Forbidden types per position: test_bad_value_position, test_bad_lower_position, test_bad_upper_position (True/False/SubInt/float/string/None)
# 3. Type-validation precedence: test_type_precedence_with_string_value_and_reversed_bounds, test_type_precedence_with_boolean_lower_and_reversed_bounds

# Limitations:
# - Does not claim exhaustive coverage beyond acceptance requirements.
# - Assumes clamp_integer exists in 'clamp_value' module with correct signature.
# - Uses pytest.raises to handle exception-based assertions correctly.
# - Does not inspect, mock, or edit implementation under test.
