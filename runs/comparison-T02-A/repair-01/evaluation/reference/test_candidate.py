import pytest
from clock_parser import minute_of_day


class _FakeStr(str):
    """A subclass of str used to verify type checking requirements."""
    pass


@pytest.mark.parametrize("text,expected", [
    ("00:00", 0),
    ("12:30", 750),
    ("23:59", 1439),
])
def test_minute_of_day_valid(text, expected):
    result = minute_of_day(text)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("text", [
    " 00:00",
    "00:00 ",
    "12:60",
    "24:00",
    "99:99",
    "0:00",
    "00:0",
    "\uff10\uff11:\uff12\uff13",
])
def test_minute_of_day_invalid_format(text):
    with pytest.raises(ValueError):
        minute_of_day(text)


@pytest.mark.parametrize("text", [
    None,
    1230,
    b"00:00",
    _FakeStr("00:00"),
])
def test_minute_of_day_invalid_type(text):
    with pytest.raises(TypeError):
        minute_of_day(text)


# Requirement-to-input mapping
# Valid inputs: ASCII "HH:MM" where H in 0..23, M in 0..59. Assertions:
#   - type(result) is int (exact built-in int check, not isinstance())
#   - result == expected numeric value (midnight=0, end-of-day=1439)

# Invalid format inputs: whitespace padding, invalid minutes (60+), hours >23, 
#   insufficient digits, Unicode fullwidth digits. Assertions:
#   - all raise ValueError exception observed via pytest.raises(ValueError)

# Invalid type inputs: None, int, bytes, str subclasses. Assertions:
#   - all raise TypeError exception observed via pytest.raises(TypeError)


# Limitations
# - These tests do not examine the internal validation sequence or order of 
#   checks performed by minute_of_day implementation.
# - Exception types are asserted at runtime observation level; internal 
#   type-check operations are not verified by test structure alone.
# - Coverage is finite: only specified cases in parametrized lists are tested.
# - Unexamined edge cases include signed zero strings ("00:-00"), negative-hour 
#   inputs, or implementation-dependent parsing behaviors beyond ASCII HH:MM bounds.
