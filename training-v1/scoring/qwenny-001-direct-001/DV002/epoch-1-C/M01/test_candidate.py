from subject import minute_of_day

import pytest


class TestTypeError:
    """Tests rejecting non-str types before any value/shape checks."""

    def test_list(self):
        with pytest.raises(TypeError):
            minute_of_day(["09:30"])

    def test_int(self):
        with pytest.raises(TypeError):
            minute_of_day(930)

    def test_float(self):
        with pytest.raises(TypeError):
            minute_of_day(9.5)

    def test_bytes(self):
        with pytest.raises(TypeError):
            minute_of_day(b"09:30")

    def test_none(self):
        with pytest.raises(TypeError):
            minute_of_day(None)

    def test_subclass_str(self, capsys):
        class MyStr(str):
            pass
        
        obj = MyStr("09:30")
        with pytest.raises(TypeError):
            minute_of_day(obj)

    def test_bool(self):
        # bool is subclass of int in Python, but should fail type check for str
        with pytest.raises(TypeError):
            minute_of_day(True)


class TestValueError:
    """Tests validating specific malformed strings."""

    def test_length_short(self):
        with pytest.raises(ValueError):
            minute_of_day("9:30")

    def test_length_long(self):
        with pytest.raises(ValueError):
            minute_of_day("09:30:00")

    def test_wrong_colon_count(self):
        with pytest.raises(ValueError):
            minute_of_day("9-30")

    def test_invalid_hour_24(self):
        with pytest.raises(ValueError):
            minute_of_day("24:00")

    def test_invalid_hour_negative(self):
        with pytest.raises(ValueError):
            minute_of_day("-1:00")

    def test_invalid_minute_high(self):
        with pytest.raises(ValueError):
            minute_of_day("00:60")

    def test_invalid_minute_low(self):
        with pytest.raises(ValueError):
            minute_of_day("00:-1")

    def test_unicode_digits(self):
        with pytest.raises(ValueError):
            minute_of_day("۰۹:۳۰")  # Arabic-Indic digits

    def test_leading_spaces(self):
        with pytest.raises(ValueError):
            minute_of_day(" 09:30")

    def test_trailing_spaces(self):
        with pytest.raises(ValueError):
            minute_of_day("09:30 ")

    def test_uppercase_letters(self):
        with pytest.raises(ValueError):
            minute_of_day("0G:3H")

    def test_reversed_bounds_logic_check(self):
        """Verify that a reversed-bounds concept (e.g., hour > 23 or minute > 59) raises ValueError."""
        # Explicitly testing hour=24, which exceeds 23
        with pytest.raises(ValueError):
            minute_of_day("24:00")


class TestSuccessCases:
    """Tests valid inputs returning exact int."""

    def test_midnight(self):
        result = minute_of_day("00:00")
        assert result == 0
        assert isinstance(result, int)
        assert not isinstance(result, bool)

    def test_noon(self):
        result = minute_of_day("12:00")
        assert result == 720
        assert isinstance(result, int)

    def test_max_valid_time(self):
        result = minute_of_day("23:59")
        assert result == 1439
        assert isinstance(result, int)

    def test_zero_minutes_non_zero_hour(self):
        result = minute_of_day("05:00")
        assert result == 300
        assert isinstance(result, int)

    def test_minute_boundary_59(self):
        result = minute_of_day("10:59")
        assert result == 659
        assert isinstance(result, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
