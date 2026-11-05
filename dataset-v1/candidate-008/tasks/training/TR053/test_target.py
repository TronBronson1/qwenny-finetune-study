import pytest
from subject import format_cents

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), '0.00', id="v000"),
    pytest.param((1,), '0.01', id="v001"),
    pytest.param((-1,), '-0.01', id="v002"),
    pytest.param((99,), '0.99', id="v003"),
    pytest.param((100,), '1.00', id="v004"),
    pytest.param((-100,), '-1.00', id="v005"),
    pytest.param((12345,), '123.45', id="v006"),
    pytest.param((1000000000000000000000000000001,), '10000000000000000000000000000.01', id="v007"),
    pytest.param((-12345,), '-123.45', id="v008"),
])
def test_values(args,expected):
    actual=format_cents(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        format_cents(*args)
