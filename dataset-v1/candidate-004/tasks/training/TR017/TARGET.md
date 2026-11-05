```python
import copy
import pytest
from subject import interleave_strings

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
    pytest.param(('', ''), '', ('', ''), id="v000"),
    pytest.param(('a', ''), 'a', ('a', ''), id="v001"),
    pytest.param(('', 'b'), 'b', ('', 'b'), id="v002"),
    pytest.param(('ab', '12'), 'a1b2', ('ab', '12'), id="v003"),
    pytest.param(('abc', '1'), 'a1bc', ('abc', '1'), id="v004"),
    pytest.param(('a', '123'), 'a123', ('a', '123'), id="v005"),
    pytest.param(('é字', ' X'), 'é 字X', ('é字', ' X'), id="v006"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=interleave_strings(*args)
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
        interleave_strings(*args)
```

Explicit return/post-state cases v000–v006 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
