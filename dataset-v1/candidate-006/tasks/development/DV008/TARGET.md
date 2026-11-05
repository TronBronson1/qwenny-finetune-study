```python
import copy
import pytest
from subject import edit_distance

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
    pytest.param(('', ''), 0, id="v000"),
    pytest.param(('', 'abc'), 3, id="v001"),
    pytest.param(('abc', ''), 3, id="v002"),
    pytest.param(('cat', 'cat'), 0, id="v003"),
    pytest.param(('cat', 'cut'), 1, id="v004"),
    pytest.param(('ab', 'ba'), 2, id="v005"),
    pytest.param(('kitten', 'sitting'), 3, id="v006"),
    pytest.param(('é', 'e'), 1, id="v007"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=edit_distance(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

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
        edit_distance(*args)
```

Explicit return/post-state cases v000–v007 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
