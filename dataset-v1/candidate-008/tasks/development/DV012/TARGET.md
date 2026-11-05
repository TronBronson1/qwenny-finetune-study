```python
import pytest
from subject import balanced_brackets

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), True, id="v000"),
    pytest.param(('()',), True, id="v001"),
    pytest.param(('([]{})',), True, id="v002"),
    pytest.param(('([)]',), False, id="v003"),
    pytest.param(('(',), False, id="v004"),
    pytest.param((']',), False, id="v005"),
    pytest.param(('}{',), False, id="v006"),
    pytest.param(('[](){}',), True, id="v007"),
])
def test_values(args,expected):
    actual=balanced_brackets(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((['('],), id="e006"),
    pytest.param((StrChild('(a)'),), id="e007"),
    pytest.param((StrChild(' '),), id="e008"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        balanced_brackets(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('(a)',), id="e004"),
    pytest.param((' ',), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        balanced_brackets(*args)
```

Return cases: empty=v000; single-pair=v001; nested-all-kinds=v002; mismatched=v003; unclosed=v004; premature-close=v005; reversed=v006; concatenated=v007. Validation cases: TypeError=e000,e001,e002,e003,e006,e007,e008; ValueError=e004,e005. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
