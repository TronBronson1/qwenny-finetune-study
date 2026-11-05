import copy
import pytest
from subject import batches
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
    pytest.param((0, 3), 0),
    pytest.param((1, 3), 1),
    pytest.param((3, 3), 1),
    pytest.param((4, 3), 2),
    pytest.param((7, 1), 7),
    pytest.param((1000000000000000000000000000000, 3), 333333333333333333333333333334),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=batches(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True, 3)),
    pytest.param((IntChild(0), 3)),
    pytest.param((1.5, 3)),
    pytest.param(('bad', 3)),
    pytest.param((None, 3)),
    pytest.param((0, True)),
    pytest.param((0, IntChild(3))),
    pytest.param((0, 1.5)),
    pytest.param((0, 'bad')),
    pytest.param((0, None)),
    pytest.param(('bad', 0)),
    pytest.param((-1, 'bad')),
    pytest.param((IntChild(-1), 3)),
    pytest.param((-1, IntChild(3))),
    pytest.param((IntChild(2), 0)),
    pytest.param((2, IntChild(0))),
    pytest.param((IntChild(2), -1)),
    pytest.param((2, IntChild(-1))),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        batches(*args)
@pytest.mark.parametrize("args", [
    pytest.param((-1, 3)),
    pytest.param((2, 0)),
    pytest.param((2, -1)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        batches(*args)
