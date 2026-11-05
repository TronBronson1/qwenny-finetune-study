from subject import minute_of_day
import pytest


class TestMinuteOfDayTypes:
    def test_valid_str_returns_int(self):
        hour, minute = 12, 30
        value = f"{hour:02d}:{minute:02d}"
        result = minute_of_day(value)
        assert isinstance(result, int)
        assert result == hour * 60 + minute

    def test_non_str_raises_type_error(self):
        cases = [
            (1234, 5678),
            (12, 34, "int, int"),
            ("12:34", 56, "str, int"),
            (None, None, "None"),
            ([12, 34], None, "list"),
            (f"{'x':12}:{'y':34}", None, "unicode string"),
        ]

        for arg, _, desc in cases:
            with pytest.raises(TypeError):
                minute_of_day(arg)


class TestMinuteOfDayValues:
    @pytest.mark.parametrize("arg", [
        "00:00", "00:01", "01:00", "12:00", "23:59", "00:59", "23:00"
    ])
    def test_edge_cases_valid(self, arg):
        result = minute_of_day(arg)
        h = int(arg[:2])
        m = int(arg[3:])
        assert result == h * 60 + m

    @pytest.mark.parametrize("arg", [
        "24:00", "00:60", "13:00x", "1:2", "23:59 ", "12 30", "12-30", "12:3"
    ])
    def test_malformed_strings_raise_value_error(self, arg):
        with pytest.raises(ValueError):
            minute_of_day(arg)


class TestMutability:
    def test_input_not_mutated(self):
        original = "12:34"
        minute_of_day(original)
        assert original == "12:34"
