```python
import pytest
from subject import count_ascii_categories

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), (0, 0, 0), id="v000"),
    pytest.param(('AbZz09',), (4, 2, 0), id="v001"),
    pytest.param(('a 1!',), (1, 1, 2), id="v002"),
    pytest.param(('é١',), (0, 0, 2), id="v003"),
    pytest.param(('\n\t',), (0, 0, 2), id="v004"),
])
def test_values(args,expected):
    actual=count_ascii_categories(*args)
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
        count_ascii_categories(*args)
```

Return cases: empty=v000; ascii-letters-digits=v001; mixed=v002; unicode-other=v003; whitespace-other=v004. Validation cases: TypeError=e000,e001,e002,e003. Exact returned types are checked recursively where specified. These finite witnesses do not prove exhaustive correctness. No execution is claimed.
