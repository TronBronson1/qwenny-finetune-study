```python
import pytest
from subject import parenthesis_depth

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), 0, id="v000"),
    pytest.param(('()',), 1, id="v001"),
    pytest.param(('(())',), 2, id="v002"),
    pytest.param(('()()',), 1, id="v003"),
    pytest.param(('(()(()))',), 3, id="v004"),
])
def test_values(args,expected):
    actual=parenthesis_depth(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((['('],), id="e008"),
    pytest.param((StrChild('('),), id="e009"),
    pytest.param((StrChild(')'),), id="e010"),
    pytest.param((StrChild(')('),), id="e011"),
    pytest.param((StrChild('(a)'),), id="e012"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parenthesis_depth(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('(',), id="e004"),
    pytest.param((')',), id="e005"),
    pytest.param((')(',), id="e006"),
    pytest.param(('(a)',), id="e007"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parenthesis_depth(*args)
```

Return cases: empty=v000; one-pair=v001; nested=v002; siblings=v003; deep=v004. Validation cases: TypeError=e000,e001,e002,e003,e008,e009,e010,e011,e012; ValueError=e004,e005,e006,e007. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
