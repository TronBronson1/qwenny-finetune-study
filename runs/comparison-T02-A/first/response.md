```python
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
```

### Requirement-to-Input Mapping
- **Valid Inputs**: ASCII strings matching `HH:MM` where H∈{0..23} and M∈{0..59}. Maps to return value `hour * 60 + minute`.
- **Invalid Format Inputs**: Strings violating length, character set (whitespace, non-digits, unicode), or numeric bounds (H > 23, M > 59). Maps to `ValueError`.
- **Invalid Type Inputs**: Non-str types (None, int, bytes) and str subclasses. Maps to `TypeError`.

### Limitations
- The tests are designed based on the provided contract but have not been executed in an environment where `clock_parser` is available.
- Coverage of specific edge cases (e.g., negative zero formatting) is inferred from standard validation patterns and may vary if the implementation differs from the specification.
- One exception case does not prove all validation orderings; distinct tests are provided for type vs format errors.
