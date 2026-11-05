import copy
import pytest
from subject import plural_count

class IntChild(int): pass
class StrChild(str): pass

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
    pytest.param((0, 'cat'), '0 cats', id="v000"),
    pytest.param((1, 'cat'), '1 cat', id="v001"),
    pytest.param((2, 'cat'), '2 cats', id="v002"),
    pytest.param((1, 'box'), '1 box', id="v003"),
    pytest.param((2, 'box'), '2 boxs', id="v004"),
    pytest.param((10, 'é'), '10 és', id="v005"),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=plural_count(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before

@pytest.mark.parametrize("args", [
    pytest.param((True, 'cat'), id="e000"),
    pytest.param((IntChild(0), 'cat'), id="e001"),
    pytest.param((1.5, 'cat'), id="e002"),
    pytest.param(('bad', 'cat'), id="e003"),
    pytest.param((None, 'cat'), id="e004"),
    pytest.param((0, StrChild('cat')), id="e005"),
    pytest.param((0, b'x'), id="e006"),
    pytest.param((0, 1), id="e007"),
    pytest.param((0, None), id="e008"),
    pytest.param((IntChild(-1), 'cat'), id="e011"),
    pytest.param((-1, StrChild('cat')), id="e012"),
    pytest.param((IntChild(1), ''), id="e013"),
    pytest.param((1, StrChild('')), id="e014"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        plural_count(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1, 'cat'), id="e009"),
    pytest.param((1, ''), id="e010"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        plural_count(*args)
