```python
import copy
import pytest
from subject import escape_html

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
    pytest.param(('abc',), 'abc', ('abc',), id="v001"),
    pytest.param(('<&>',), '&lt;&amp;&gt;', ('<&>',), id="v002"),
    pytest.param(('"\'',), '&quot;&#x27;', ('"\'',), id="v003"),
    pytest.param(('&amp;',), '&amp;amp;', ('&amp;',), id="v004"),
    pytest.param(("é <a x='1'>",), 'é &lt;a x=&#x27;1&#x27;&gt;', ("é <a x='1'>",), id="v005"),
])
def test_values(args,expected,after):
    before=copy.deepcopy(args)
    actual=escape_html(*args)
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
        escape_html(*args)
```

Explicit return/post-state cases v000–v005 cover the listed contract examples and boundaries. Separate exception tuples isolate invalid types, specified invalid values and any listed type-before-value witnesses. Nested returned types are checked explicitly. These are finite cases, not exhaustive coverage or proof of correctness. No execution is claimed by this answer.
