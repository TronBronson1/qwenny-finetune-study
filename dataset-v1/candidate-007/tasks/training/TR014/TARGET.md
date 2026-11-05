```python
import pytest
from subject import collapse_spaces

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param(('a',), 'a', id="v001"),
    pytest.param(('   ',), ' ', id="v002"),
    pytest.param((' a  b ',), ' a b ', id="v003"),
    pytest.param(('a\t  b',), 'a\t b', id="v004"),
    pytest.param(('a\n  b',), 'a\n b', id="v005"),
    pytest.param(('é  字',), 'é 字', id="v006"),
    pytest.param(('a\xa0 b',), 'a\xa0 b', id="v007"),
])
def test_values(args,expected):
    actual=collapse_spaces(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        collapse_spaces(*args)
```

Return cases: empty=v000; unchanged=v001; spaces-only=v002; edges-and-run=v003; preserve-tab=v004; preserve-lf=v005; unicode=v006; preserve-nbsp=v007. Validation cases: TypeError=e000,e001,e002,e003. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
