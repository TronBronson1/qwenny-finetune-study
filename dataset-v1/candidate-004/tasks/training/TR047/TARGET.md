```python
import copy
import pytest
from subject import index_of_nth

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
    pytest.param(('', 'a', 1), -1, ('', 'a', 1), id="v000"),
    pytest.param(('aaaa', 'aa', 1), 0, ('aaaa', 'aa', 1), id="v001"),
    pytest.param(('aaaa', 'aa', 2), 1, ('aaaa', 'aa', 2), id="v002"),
    pytest.param(('aaaa', 'aa', 3), 2, ('aaaa', 'aa', 3), id="v003"),
    pytest.param(('aaaa', 'aa', 4), -1, ('aaaa', 'aa', 4), id="v004"),
    pytest.param(('abc', 'abc', 1), 0, ('abc', 'abc', 1), id="v005"),
    pytest.param(('abc', 'x', 1), -1, ('abc', 'x', 1), id="v006"),
    pytest.param(('éé', 'é', 2), 1, ('éé', 'é', 2), id="v007"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=index_of_nth(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''), 'a', 1), id="e000"),
    pytest.param((b'x', 'a', 1), id="e001"),
    pytest.param((1, 'a', 1), id="e002"),
    pytest.param((None, 'a', 1), id="e003"),
    pytest.param(('', StrChild('a'), 1), id="e004"),
    pytest.param(('', b'x', 1), id="e005"),
    pytest.param(('', 1, 1), id="e006"),
    pytest.param(('', None, 1), id="e007"),
    pytest.param(('', 'a', True), id="e008"),
    pytest.param(('', 'a', IntChild(1)), id="e009"),
    pytest.param(('', 'a', 1.5), id="e010"),
    pytest.param(('', 'a', 'bad'), id="e011"),
    pytest.param(('', 'a', None), id="e012"),
    pytest.param(('abc', '', True), id="e015"),
    pytest.param(('abc', StrChild('a'), 0), id="e016"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        index_of_nth(*args)

@pytest.mark.parametrize("args", [
    pytest.param(('abc', '', 1), id="e013"),
    pytest.param(('abc', 'a', 0), id="e014"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        index_of_nth(*args)
```

Explicit return/post-state cases v000–v007 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
