

```python
import pytest
from subject import minute_of_day


class StrSub(str):
    pass


@pytest.mark.parametrize('args', [('00:00',), ('05:30',), ('23:59',)])
def test_valid_returns(args):
    result = minute_of_day(*args)
    text = args[0]
    assert isinstance(result, int)
    assert type(result) == int
    assert isinstance(text, str)
    assert type(text) == str
    hour_part, minute_part = text.split(':')
    calculated = int(hour_part) * 60 + int(minute_part)
    assert result == calculated


@pytest.mark.parametrize('args', [
    (StrSub("00:00"),),
    ("1234",),
    ("abc:de",),
    ("24:00",),
    ("00:60",),
    ("0:00",),
])
def test_type_errors(args):
    with pytest.raises(TypeError):
        minute_of_day(*args)


@pytest.mark.parametrize('args', [
    ("24:00",),
    ("25:00",),
    ("00:60",),
    ("00:61",),
    ("00:00 ",),
])
def test_value_errors(args):
    text = args[0]
    with pytest.raises(ValueError):
        minute_of_day(text)
    # Verify reversed-bounds condition for hour/minute
    if ':' in text:
        try:
            hour = int(text[:2])
            minute =