```python
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
    result = minute_of_day(text)
    assert isinstance(result, int) and result == expected

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
    "24:00",
    "23:60",
    " 00:00",
    "00:00 ",
    "1-00:00",
    "abc:def",
    "\u0661\u0662:\u0663\u0664",
])
def test_values(text):
    with pytest.raises(ValueError):
        minute_of_day(text)
```

**Requirement-to-Input Mapping:**
*   `("00:00", 0)` and `result == expected` with `isinstance(result, int)`: validates return type is exact built-in int.
*   `("12:00", 720)` and `("23:59", 1439)`: same assertions for interior/end-of-day times.
*   `(True, False, 12, None, b"00:00", StrChild("00:00"))` with `pytest.raises(TypeError)`: all raise TypeError for invalid or subclass types.
*   `"24:00"` (hour=24), `"23:60"` (minute=60): raises ValueError for out-of-range components.
*   `" 00:00"`, `"00:00 "` (leading/trailing whitespace): raises ValueError.
*   `"1-00:00"`, `"abc:def"` (non-ASCII characters, wrong separator): raises ValueError.
*   `"\u0661\u0662:\u0663\u0664"` (Unicode digits): raises ValueError.

**Limitations:**
These finite examples do not cover all valid times or all potential malformed strings. A single exception case does not prove every validation ordering. The suite verifies TypeError and ValueError are raised appropriately, but does not establish the internal sequence of validation checks performed by the implementation. These tests were inspected; this demonstration does not claim execution. See the separate check record for actual validation status.
