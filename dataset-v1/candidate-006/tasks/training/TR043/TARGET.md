```python
import copy
import pytest
from subject import parse_binary

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
    pytest.param(('0',), 0, id="v000"),
    pytest.param(('1',), 1, id="v001"),
    pytest.param(('001',), 1, id="v002"),
    pytest.param(('1010',), 10, id="v003"),
    pytest.param(('11111111111111111111111111111111',), 4294967295, id="v004"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parse_binary(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild('0'),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((StrChild(''),), id="e008"),
    pytest.param((StrChild('2'),), id="e009"),
    pytest.param((StrChild(' 1'),), id="e010"),
    pytest.param((StrChild('111111111111111111111111111111111'),), id="e011"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parse_binary(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('',), id="e004"),
    pytest.param(('2',), id="e005"),
    pytest.param((' 1',), id="e006"),
    pytest.param(('111111111111111111111111111111111',), id="e007"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        parse_binary(*args)
```

Explicit return/post-state cases v000–v004 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
