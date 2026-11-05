```python
import pytest
from subject import ascii_upper

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param(('abcXYZ',), 'ABCXYZ', id="v001"),
    pytest.param(('z-a 9',), 'Z-A 9', id="v002"),
    pytest.param(('éßı',), 'éßı', id="v003"),
    pytest.param(('a\nb',), 'A\nB', id="v004"),
    pytest.param(('ǅ١ｅ',), 'ǅ١ｅ', id="v005"),
])
def test_values(args,expected):
    actual=ascii_upper(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((['a'],), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        ascii_upper(*args)
```

Return cases: empty=v000; ascii-case=v001; punctuation-digits=v002; nonascii-unchanged=v003; newline=v004; compatibility-characters=v005. Validation cases: TypeError=e000,e001,e002,e003,e004. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
