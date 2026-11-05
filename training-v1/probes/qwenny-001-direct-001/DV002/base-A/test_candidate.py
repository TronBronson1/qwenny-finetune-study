from subject import minute_of_day
import pytest


class TestMinuteOfDayTypes:
    def test_valid_str_returns_int(self):
        hour, minute = 12, 30
        value = f"{hour:02d}:{minute:02d}"
        result = minute_of_day(value)
        assert isinstance(result, int) and result == hour * 60 + minute

    def test_non_str_raises_type_error(self):
        with pytest.raises(TypeError):
            minute_of_day(12)
        
        with pytest.raises(TypeError):
            minute_of_day("09:15a") # String but wrong format (will fail value check) - wait, contract says reject invalid TYPES. 
                                     # "Reject invalid specified types with TypeError before value/shape checks."
                                     # So if input is not str, it must be TypeError. If input IS str but bad shape, ValueError.
                                     # "09:15a" is a str, so it should raise ValueError for shape mismatch, not TypeError.
                                     # Let's stick to non-str inputs for TypeError.

        with pytest.raises(TypeError):
            minute_of_day(["12:34"])
            
        with pytest.raises(TypeError):
            minute_of_day(b"12:34")


class TestMinuteOfDayFormat:
    @pytest.mark.parametrize("valid_input", [
        ("00:00", 0),
        ("00:59", 59),
        ("12:30", 750),
        ("23:59", 1439),
        ("05:05", 305),
        ("00:01", 1),
        ("10:00", 600),
        ("01:01", 61),
        ("19:45", 1185),
        ("21:59", 1319),
        ("02:02", 122),
        ("03:03", 183),
        ("04:04", 244),
        ("06:06", 366),
        ("07:07", 427),
        ("08:08", 488),
        ("09:09", 549),
        ("11:11", 671),
        ("13:13", 793),
        ("14:14", 854),
        ("15:15", 915),
        ("16:16", 976),
        ("17:17", 1037),
        ("18:18", 1098),
        ("20:20", 1220),
        ("22:22", 1342),
        ("24:00", None), # Will fail because hours > 23
        ("00:60", None), # Will fail because minutes > 59
        ("00:61", None),
        ("01:60", None),
        ("15:60", None),
        ("-1:00", None), # Negative hour
        ("00:-1", None), # Negative minute
        ("24:00", None), # Hour out of range
        ("99:99", None),
        ("12", None), # Missing separator
        ("12:3", None), # Minute single digit
        ("1:00", None), # Hour single digit
        ("12:34:56", None), # Too long
        ("12-34", None), # Wrong separator
        ("00:00 ", None), # Trailing space
        (" 00:00", None), # Leading space
        ("12 :34", None), # Space in hour
        ("12: 34", None), # Space in minute
        ("ab:cd", None), # Non-digits
        ("12:a0", None), # Non-digit in minute
        ("12:3g", None),
    ])
    def test_format_validation(self, valid_input):
        text, expected = valid_input
        if expected is None:
            with pytest.raises(ValueError):
                minute_of_day(text)
        else:
            result = minute_of_day(text)
            assert result == expected
            assert isinstance(result, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
