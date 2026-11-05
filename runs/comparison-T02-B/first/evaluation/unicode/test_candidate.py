import pytest
from clock_parser import minute_of_day

class StrChild(str):
    pass

@pytest.mark.parametrize("text,expected", [
    ("00:00", 0),
    ("12:00", 720),
    ("23:59", 1439),
])
def test_returns(text, expected):
    assert minute_of_day(text) == expected

@pytest.mark.parametrize("text", [
    True,
    False,
    12,
    None,
    b"00:00",
    StrChild("00:00"),
])
def test_types(text):
    with pytest.raises(TypeError):
        minute_of_day(text)

@pytest.mark.parametrize("text", [
    ("24:00"),
    ("23:60"),
    (" 00:00"),
    ("00:00 "),
    ("1-00:00"),
    ("abc:def"),
    ("٠٠:٠٠"),
])
def test_values(text):
    with pytest.raises(ValueError):
        minute_of_day(text)
