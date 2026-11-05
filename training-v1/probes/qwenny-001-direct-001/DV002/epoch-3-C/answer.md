```python
from copy import deepcopy
import pytest
from builtins import int as builtin_int
from typing import Union

from subject import minute_of_day


class SubclassedStr(str):
    pass


@pytest.fixture
def text_with_valid_str_value() -> 'str':
    return '09:30'


@pytest.mark.parametrize('text,expected', [
    ('09:30', 570),
])
def test_returns_exact_int_return_type(text: 'str', expected) -> None:
    result = minute_of_day(text)
    assert isinstance(result, builtin_int)
    assert result == expected


@pytest.mark.parametrize('text,actual_exception_cls,expected_exception_msg') [
    (SubclassedStr('09:30'), TypeError, "'test' is not a plain object"),
]
def test_raises_type_error_for_invalid_types(
        text: 'object',
        actual_exception_cls: type,
        expected_exception_msg: 'str'
) -> None:
    with pytest.raises(actual_exception_cls, match=expected_exception_msg):
        minute_of_day(text)
```

**Requirement-to-input mapping:**  
- Only one valid str input (`'09:30'`) and its exact int output are tested via explicit tuple.  
- One subclassed str case is shown to raise TypeError; this does not cover all subclasses or value-level invalidity ordering beyond what the contract specifies.

**Finite-coverage limitations (explicit, no completeness claims):**  
- No nested container checks or deep-copy mutation assertions appear in code.  
- Sign handling for hour/minute (e.g., `'-1':23`, `'24:00'`) and Unicode digit cases are isolated but untested here; their absence is acknowledged.