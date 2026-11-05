```python
import copy
import pytest
from subject import make_slug

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
    pytest.param(('',), '', id="v000"),
    pytest.param((' --_ ',), '', id="v001"),
    pytest.param(('Hello World',), 'hello-world', id="v002"),
    pytest.param((' A__b--C ',), 'a-b-c', id="v003"),
    pytest.param(('X9',), 'x9', id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=make_slug(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        make_slug(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('a/b',), id="e004"),
    pytest.param(('é',), id="e005"),
    pytest.param(('a\tb',), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        make_slug(*args)
```

Explicit return/post-state cases v000–v004 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
