```python
import copy
import pytest
from subject import collapse_spaces

class IntChild(int): pass
class StrChild(str): pass
class BytesChild(bytes): pass
class ListChild(list): pass
class TupleChild(tuple): pass
class DictChild(dict): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)
    elif type(expected) is dict:
        assert actual.keys() == expected.keys()
        assert all(type(k) is str for k in actual)
        for key in expected: assert_exact_shape(actual[key],expected[key])

@pytest.mark.parametrize("args,expected,after", [
    pytest.param(('',), '', ('',), id="v000"),
    pytest.param(('a',), 'a', ('a',), id="v001"),
    pytest.param(('   ',), ' ', ('   ',), id="v002"),
    pytest.param((' a  b ',), ' a b ', (' a  b ',), id="v003"),
    pytest.param(('a\t  b',), 'a\t b', ('a\t  b',), id="v004"),
    pytest.param(('a\n  b',), 'a\n b', ('a\n  b',), id="v005"),
    pytest.param(('é  字',), 'é 字', ('é  字',), id="v006"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=collapse_spaces(*args)
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
        collapse_spaces(*args)
```

Explicit return/post-state cases v000–v006 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
