import pytest
from subject import quote_csv_field

class StrChild(str): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param(('',), '""', id="v000"),
    pytest.param(('abc',), 'abc', id="v001"),
    pytest.param(('a,b',), '"a,b"', id="v002"),
    pytest.param(('a"b',), '"a""b"', id="v003"),
    pytest.param(('a\rb',), '"a\rb"', id="v004"),
    pytest.param(('a\nb',), '"a\nb"', id="v005"),
    pytest.param((' a ',), ' a ', id="v006"),
    pytest.param(('é',), 'é', id="v007"),
])
def test_values(args,expected):
    actual=quote_csv_field(*args)
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
        quote_csv_field(*args)
