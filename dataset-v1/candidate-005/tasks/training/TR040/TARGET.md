```python
import copy
import pytest
from subject import parse_key_value

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected", [
    pytest.param(('a=b',), ('a', 'b'), id="v000"),
    pytest.param(('a=',), ('a', ''), id="v001"),
    pytest.param(('a=b=c',), ('a', 'b=c'), id="v002"),
    pytest.param((' a = b ',), (' a ', ' b '), id="v003"),
    pytest.param(('é=字',), ('é', '字'), id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_key_value(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('a=b'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_key_value(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('a',), id="e004"),
    pytest.param(('=a',), id="e005"),
    pytest.param(('',), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_key_value(*args)
```

Explicit return/post-state cases v000–v004 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
