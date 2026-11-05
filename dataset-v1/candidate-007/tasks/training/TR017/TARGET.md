```python
import pytest
from subject import interleave_strings

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('', ''), '', id="v000"),
    pytest.param(('a', ''), 'a', id="v001"),
    pytest.param(('', 'b'), 'b', id="v002"),
    pytest.param(('ab', '12'), 'a1b2', id="v003"),
    pytest.param(('abc', '1'), 'a1bc', id="v004"),
    pytest.param(('a', '123'), 'a123', id="v005"),
    pytest.param(('é字', ' X'), 'é 字X', id="v006"),
])
def test_values(args,expected):
    actual=interleave_strings(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''), ''), id="e000"),
    pytest.param((b'x', ''), id="e001"),
    pytest.param((1, ''), id="e002"),
    pytest.param((None, ''), id="e003"),
    pytest.param(('', StrChild('')), id="e004"),
    pytest.param(('', b'x'), id="e005"),
    pytest.param(('', 1), id="e006"),
    pytest.param(('', None), id="e007"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        interleave_strings(*args)
```

Return cases: both-empty=v000; right-empty=v001; left-empty=v002; equal-length=v003; left-remainder=v004; right-remainder=v005; unicode-space=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
