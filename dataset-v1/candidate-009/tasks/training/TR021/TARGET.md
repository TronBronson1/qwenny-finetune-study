```python
import pytest
from subject import common_prefix

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('', ''), '', id="v000"),
    pytest.param(('', 'a'), '', id="v001"),
    pytest.param(('abc', 'abc'), 'abc', id="v002"),
    pytest.param(('abc', 'abd'), 'ab', id="v003"),
    pytest.param(('abc', 'a'), 'a', id="v004"),
    pytest.param(('Ab', 'ab'), '', id="v005"),
    pytest.param(('é字a', 'é字b'), 'é字', id="v006"),
])
def test_values(args,expected):
    actual=common_prefix(*args)
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
        common_prefix(*args)
```

Return cases: both-empty=v000; left-empty=v001; equal=v002; partial=v003; shorter-right=v004; case-sensitive=v005; unicode=v006. Validation cases: TypeError=e000,e001,e002,e003,e004,e005,e006,e007. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
