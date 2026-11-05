```python
import pytest
from subject import count_vowels

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), 0, id="v000"),
    pytest.param(('AEIOUaeiou',), 10, id="v001"),
    pytest.param(('rhythm',), 0, id="v002"),
    pytest.param(('Apple pie',), 4, id="v003"),
    pytest.param(('éÁy',), 0, id="v004"),
    pytest.param(('a1 E!',), 2, id="v005"),
])
def test_values(args,expected):
    actual=count_vowels(*args)
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
        count_vowels(*args)
```

Return cases: empty=v000; both-ascii-cases=v001; no-vowels=v002; mixed-text=v003; exclude-accent-y=v004; digits-punctuation=v005. Validation cases: TypeError=e000,e001,e002,e003. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
