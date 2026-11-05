import pytest
from subject import parity_label

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), 'even', id="v000"),
    pytest.param((1,), 'odd', id="v001"),
    pytest.param((2,), 'even', id="v002"),
    pytest.param((-1,), 'odd', id="v003"),
    pytest.param((-2,), 'even', id="v004"),
    pytest.param((1000000000000000000000000000001,), 'odd', id="v005"),
])
def test_values(args,expected):
    actual=parity_label(*args)
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
        parity_label(*args)
