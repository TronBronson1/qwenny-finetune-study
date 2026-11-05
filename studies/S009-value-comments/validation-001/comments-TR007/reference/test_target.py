import pytest
from subject import digit_sum

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((0,), 0, id="v000"), # 0 = 0
    pytest.param((7,), 7, id="v001"), # 7 = 7
    pytest.param((10,), 1, id="v002"), # 1+0 = 1
    pytest.param((101,), 2, id="v003"), # 1+0+1 = 2
    pytest.param((999,), 27, id="v004"), # 9+9+9 = 27
    pytest.param((1000000000000000000000000000007,), 8, id="v005"), # 1+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+7 = 8
])
def test_values(args,expected):
    actual=digit_sum(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(0),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((IntChild(-1),), id="e006"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        digit_sum(*args)

@pytest.mark.parametrize("args", [
    pytest.param((-1,), id="e005"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        digit_sum(*args)
