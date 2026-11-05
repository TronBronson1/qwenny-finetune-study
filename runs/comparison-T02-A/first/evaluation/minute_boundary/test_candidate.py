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
    assert minute_of_day(text) == expected


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
