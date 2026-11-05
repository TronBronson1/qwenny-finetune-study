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
```

**Requirement-to-Input Mapping:**
*   **Input**: Exact built-in `str` representing time.
*   **Output**: Built-in `int` (minutes from midnight).
*   **Validation Order**: Type checks (`isinstance(str)` and subclass rejection) precede value checks (format and range).

**Limitations:**
This demonstration covers specific valid timestamps, invalid types, and invalid values. Finite cases do not cover all 1440 minutes or all potential malformed strings. Subclass instances are explicitly checked but not all Python subclasses enumerated. Type precedence logic is verified for a single argument where type errors take priority over value checks; this does not guarantee the exact internal validation order of every implementation detail (e.g., specific exception class hierarchy if implemented otherwise). Execution status: Inspected, not executed.
