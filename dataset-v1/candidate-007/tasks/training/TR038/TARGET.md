```python
import pytest
from subject import parse_hex_byte

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('00',), 0, id="v000"),
    pytest.param(('09',), 9, id="v001"),
    pytest.param(('0a',), 10, id="v002"),
    pytest.param(('Af',), 175, id="v003"),
    pytest.param(('FF',), 255, id="v004"),
    pytest.param(('80',), 128, id="v005"),
])
def test_values(args,expected):
    actual=parse_hex_byte(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('00'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild(''),), id="e011"),
    pytest.param((StrChild('f'),), id="e012"),
    pytest.param((StrChild('000'),), id="e013"),
    pytest.param((StrChild('g0'),), id="e014"),
    pytest.param((StrChild(' ff'),), id="e015"),
    pytest.param((StrChild('٣f'),), id="e016"),
    pytest.param((StrChild('３f'),), id="e017"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_hex_byte(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('f',), id="e005"),
    pytest.param(('000',), id="e006"),
    pytest.param(('g0',), id="e007"),
    pytest.param((' ff',), id="e008"),
    pytest.param(('٣f',), id="e009"),
    pytest.param(('３f',), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_hex_byte(*args)
```

Return cases: zero=v000; decimal-digits=v001; lowercase=v002; mixed-case=v003; byte-upper-bound=v004; intermediate=v005. Validation cases: TypeError=e000,e001,e002,e003,e011,e012,e013,e014,e015,e016,e017; ValueError=e004,e005,e006,e007,e008,e009,e010. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
