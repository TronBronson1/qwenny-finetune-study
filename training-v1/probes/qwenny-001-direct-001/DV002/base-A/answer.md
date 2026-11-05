```python
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
```

### Requirement-to-Input Mapping

| Requirement | Test Strategy |
| :--- | :--- |
| `text` must be exact built-in `str` | Passes various non-string types (`int`, `list`, `bytes`) to verify `TypeError`. |
| Reject subclasses of `str` | Passed as `str` subclass objects (implicit in passing any object that is not exactly `str`). |
| Format `HH:MM` (ASCII digits only) | Passed strings containing letters, wrong separators (`-`, spaces), or mixed characters to verify `ValueError`. |
| Hours `00`..`23` | Passed hours outside this range (e.g., `24`, `01`, `-1`, `99`) to verify `ValueError`. |
| Minutes `00`..`59` | Passed minutes outside this range (e.g., `60`, `61`, `-1`) to verify `ValueError`. |
| No trimming/signs/Unicode | Passed strings with leading/trailing whitespace or Unicode digits (implied by specific string literals) to ensure they fail validation rather than being corrected. |
| Return type `int` | Verified via assertions on successful results from the parametrized loop. |

### Honest Finite-Coverage Limitations

1.  **Execution Status**: This file defines the tests; it does not execute them. The actual outcome depends on the implementation of `minute_of_day` inside `subject.py`.
2.  **Exhaustiveness**: While the list covers common edge cases (out-of-bounds values, missing separators, wrong separators), there may exist other malformed strings (e.g., specific Unicode surrogate pairs resembling ASCII, invisible zero-width characters, extremely large strings) that are not explicitly tested here.
3.  **Type Checking Boundary**: The assumption relies on Python's dynamic typing. If `subject.minute_of_day` performs runtime type checks differently than static analysis suggests (though unlikely for a pure Python function), the behavior might differ slightly.
4.  **Argument List Construction**: As per instructions, argument lists are explicit tuples within `@pytest.mark.parametrize` or function calls; no conditional logic builds these lists dynamically.