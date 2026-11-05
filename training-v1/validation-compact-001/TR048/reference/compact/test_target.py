import copy
import pytest
from subject import spreadsheet_column
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
    pytest.param((1,), 'A'),
    pytest.param((26,), 'Z'),
    pytest.param((27,), 'AA'),
    pytest.param((52,), 'AZ'),
    pytest.param((702,), 'ZZ'),
    pytest.param((703,), 'AAA'),
    pytest.param((18278,), 'ZZZ'),
])
def test_values(args,expected):
    before=copy.deepcopy(args)
    actual=spreadsheet_column(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)
    assert args == before
@pytest.mark.parametrize("args", [
    pytest.param((True,)),
    pytest.param((IntChild(1),)),
    pytest.param((1.5,)),
    pytest.param(('bad',)),
    pytest.param((None,)),
    pytest.param((IntChild(0),)),
    pytest.param((IntChild(18279),)),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        spreadsheet_column(*args)
@pytest.mark.parametrize("args", [
    pytest.param((0,)),
    pytest.param((18279,)),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        spreadsheet_column(*args)
