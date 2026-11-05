import pytest
from subject import spreadsheet_column

class IntChild(int): pass

def assert_exact_shape(actual, expected):
    assert type(actual) is type(expected)
    if type(expected) in (list,tuple):
        assert len(actual) == len(expected)
        for a,b in zip(actual,expected): assert_exact_shape(a,b)

@pytest.mark.parametrize("args,expected", [
    pytest.param((1,), 'A', id="v000"),
    pytest.param((26,), 'Z', id="v001"),
    pytest.param((27,), 'AA', id="v002"),
    pytest.param((52,), 'AZ', id="v003"),
    pytest.param((702,), 'ZZ', id="v004"),
    pytest.param((703,), 'AAA', id="v005"),
    pytest.param((18278,), 'ZZZ', id="v006"),
])
def test_values(args,expected):
    actual=spreadsheet_column(*args)
    assert actual == expected
    assert_exact_shape(actual,expected)

@pytest.mark.parametrize("args", [
    pytest.param((True,), id="e000"),
    pytest.param((IntChild(1),), id="e001"),
    pytest.param((1.5,), id="e002"),
    pytest.param(('bad',), id="e003"),
    pytest.param((None,), id="e004"),
    pytest.param((-1.5,), id="e007"),
    pytest.param((IntChild(0),), id="e008"),
    pytest.param((IntChild(18279),), id="e009"),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        spreadsheet_column(*args)

@pytest.mark.parametrize("args", [
    pytest.param((0,), id="e005"),
    pytest.param((18279,), id="e006"),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        spreadsheet_column(*args)
