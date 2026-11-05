import copy
import pytest
from subject import parity_label
class IntChild(int): pass
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
    pytest.param((0,), 'even'),
    pytest.param((1,), 'odd'),
    pytest.param((2,), 'even'),
    pytest.param((-1,), 'odd'),
    pytest.param((-2,), 'even'),
    pytest.param((1000000000000000000000000000001,), 'odd'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=parity_label(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True,)),
    pytest.param((IntChild(0),)),
    pytest.param((1.5,)),
    pytest.param(('bad',)),
    pytest.param((None,)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        parity_label(*args)
