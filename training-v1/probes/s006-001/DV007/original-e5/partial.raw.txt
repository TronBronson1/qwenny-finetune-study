```python
import copy
import pytest
from subject import grid_neighbors

class IntChild(int): pass

@pytest.mark.parametrize("args,expected", [
    ( (0,0,1,1), [ (1,0) ] ),
    ( (1,0,2,2), [ (1,1), (2,0), (0,0) ] ),
    ( (0,0,2,2), [ (1,0) ] ),
])
def test_values(args,expected):
    before,args_copy=copy.deepcopy(args),args
    actual=value=grid_neighbors(*args)
    assert actual==expected and type(actual) is type(expected) and args==args_copy

@pytest.mark.parametrize("args", [
    (True,0,1,1),
    (0,True,1,1),
    (0,0,True,1),
    (0,0,1,True),
    (0.0,0,1,1),
    (0,0.0,1,1),
    (0,0,0.0,1),
    (0,0,1,0.0),
    (IntChild(0),0,1,1),
    (0,IntChild(0),1,1),
    (0,0,IntChild(0),1),
    (0,0,1,IntChild(0)),
    (b'0',0,1,1),
    (None,0,1,1),
    (0,None,1,1),
    (0,0,None,1),
    (0,0,1,None),
    ( [],0,1,1 ),
    ( (0,0,0,0), ),
])
def test_raises_typeerror(args):
    with pytest.raises(TypeError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    ( -1,0,1,1 ),
    ( 0,-1,1,1 ),
    ( 0,0,-1,1 ),
    ( 0,0,0,1 ),
    ( 0,0,0,0 ),
])
def test_raises_valueerror(args):
    with pytest.raises(ValueError):
        grid_neighbors(*args)

@pytest.mark.parametrize("args", [
    ( 1,1,2,2 ),
    ( 0,2,2,2 ),
    ( 2,0,2,2 ),
    ( 2,2,2,2 ),
])
def test_raises_indexerror(args):
    with pytest.raises(IndexError):
        grid_neighbors(*args)
```

Explicit return/post-state cases cover the listed valued asserted tuples and types before/after each asserted value test. Separate exception cases isolate invalid types, specified invalid values and any listed type-before witnesses. No exhaustiveness or recursion-coverage claim. No execution is performed by this answer.