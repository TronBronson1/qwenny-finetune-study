import pytest
from subject import escape_html

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '', id="v000"),
    pytest.param(('abc',), 'abc', id="v001"),
    pytest.param(('<&>',), '&lt;&amp;&gt;', id="v002"),
    pytest.param(('"\'',), '&quot;&#x27;', id="v003"),
    pytest.param(('&amp;',), '&amp;amp;', id="v004"),
    pytest.param(("é <a x='1'>",), 'é &lt;a x=&#x27;1&#x27;&gt;', id="v005"),
])
def test_values(args,expected):
    actual=escape_html(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((StrChild(''),), id="e000"),
    pytest.param((b'x',), id="e001"),
    pytest.param((1,), id="e002"),
    pytest.param((None,), id="e003"),
    pytest.param((['a'],), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        escape_html(*args)
