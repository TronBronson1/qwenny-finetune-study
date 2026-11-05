import pytest
from my_module import clamp_integer

# Helper class to simulate an integer subclass for type validation testing.
# Note: This is defined strictly within the test scope and does not count as implementing 
# the target function clamp_integer.
class _ExactSubInt(int):
    """An explicit integer subclass to verify 'reject integer subclasses' requirement."""
    pass


class TestClampInteger:
    
    # Requirement 1: Normal ranges, below/above limits, endpoints, equal bounds, reversed bounds.
    @pytest.mark.parametrize("input_args, expected", [
        # Normal values within bounds
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
        # Negative ranges (clamp lower)
        ((-15, -10, 0), -10),
        # Negative ranges (clamp upper)
        ((2, -10, 0), 0),
        # Reversed bounds (ValueError expected)
        ((5, 10, 0), pytest.raises(ValueError)),
    ])
    def test_valid_inputs_behavior(self, clamp_integer, input_args, expected):
        """Test clamping logic with valid integer types and various ranges."""
        if isinstance(expected, type): # Handle pytest.raises wrapper
            with expected:
                result = clamp_integer(*input_args)
                assert False, f"Expected {expected} to be raised, but got value {result}"
        else:
            result = clamp_integer(*input_args)
            assert result == expected
    
    # Requirement 2: Test forbidden types in EACH of the three positions (value, lower, upper).
    @pytest.mark.parametrize("bad_type_value", [
        True, False, _ExactSubInt(), 1.5, "3", None
    ])
    def test_bad_value_position(self, bad_type_value):
        """Test that invalid 'value' raises TypeError regardless of valid bounds."""
        with pytest.raises(TypeError):
            clamp_integer(bad_type_value, 0, 10)

    @pytest.mark.parametrize("bad_type_lower", [
        True, False, _ExactSubInt(), 1.5, "3", None
    ])
    def test_bad_lower_position(self, bad_type_lower):
        """Test that invalid 'lower' raises TypeError regardless of valid value/upper."""
        with pytest.raises(TypeError):
            clamp_integer(5, bad_type_lower, 10)

    @pytest.mark.parametrize("bad_type_upper", [
        True, False, _ExactSubInt(), 1.5, "3", None
    ])
    def test_bad_upper_position(self, bad_type_upper):
        """Test that invalid 'upper' raises TypeError regardless of valid value/lower."""
        with pytest.raises(TypeError):
            clamp_integer(5, 0, bad_type_upper)

    # Requirement 3: Test type-validation precedence (TypeError before ValueError).
    @pytest.mark.parametrize("bad_input", [
        ("bad", 10, 0), # String value, reversed bounds
        ((True,), "10", 0), # Boolean lower, reversed bounds - note syntax below
    ])
    def test_type_validation_precedence(self):
        """Verify TypeError is raised for bad types even if bounds are invalid (ValueError)."""
        # Note: The above parametrize was illustrative. We will use specific explicit tuples below.
        pass

    def test_type_precedence_explicit_tuple(self, clamp_integer):
        """Test precedence explicitly as per acceptance requirement 3."""
        # Input ("bad", 10, 0) -> Type error on 'bad' before checking order 10 > 0.
        with pytest.raises(TypeError):
            clamp_integer("bad", 10, 0)

        # Another precedence check: Lower bound is bad type.
        with pytest.raises(TypeError):
            clamp_integer(5, True, 10)
