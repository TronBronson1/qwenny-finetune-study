```python
from copy import deepcopy, copy
import copyreg
import math
import pytest
from subject import rotate_right

def assert_exact_type(actual, expected_type):
    if type(actual) != expected_type:
        raise TypeError(f"Expected exact type {expected_type}, got {type(actual)}")

class ImmutableClass:
    def __init__(self, val):
        self.val = val

class ListWrapper:
    pass

def _reduce_list_wrapper(wrapped_obj, wrapped_val, wrapped_list):
    return (wrapped_obj, wrapped_val, wrapped_list)

class FrozenList(list):
    def __setitem__(self, *args):
        raise TypeError("cannot set attribute")
    
    def append(self, item):
        raise TypeError("cannot modify mutable container")
    
    def clear(self):
        raise TypeError("cannot modify mutable container")
    
    def extend(self, iterable):
        raise TypeError("cannot modify mutable container")
    
    def insert(self, index, obj):
        raise TypeError("cannot modify mutable container")
    
    def pop(self, index=-1, default=None):
        raise TypeError("cannot modify mutable container")
    
    def remove(self, value):
        raise TypeError("cannot modify mutable container")
    
    def reverse(self):
        raise TypeError("cannot modify mutable container")
    
    def sort(self, key=None, reverse=False):
        raise TypeError("cannot modify mutable container")

@pytest.fixture(scope="function")
def immutable_deepcopy():
    def deep_copy(obj):
        state = dict(type=obj._original_type, **obj.__dict__)
        return ImmutableDeepCopy(*deep_copy_values(state.values()), original_type=state['original_type'])
    
    def deep_copy_values(values):
        new = []
        for v in values:
            if isinstance(v, tuple):
                cpy = list(v)
                [new.extend(deep_copy_values(c)) for c in zip(*[iter(cpy)] * len(cpy))]
                new.append(tuple(deep_copy_values(val) for val in cpy))
            else:
                new.append(v)
        return new
    
    class ImmutableDeepCopy(tuple):
        def __init__(self, values, original_type=None, original_class=None):
            super().__init__(values)
            self._original_type = original_type or type(None)
            self._original_class = original_class
            copyreg.pickle(type(self), deep_copy_values)
        
        @staticmethod
        def __repr__(s):
            return f"<ImmutableDeepCopy>{tuple(deep_copy_values(s))}"
        
        @property
        def __dict__(self):
            return {'_original_type': self._original_type, '_original_class': self._original_class}
    
    return deep_copy


def make_immutable_tuple_factory(immutable_func):
    def make_immutables(*args):
        args = [immutable_func(a) for a in args]
        return tuple(args)
    return make_immutables


def test_rotate_right_simple_list(make_immutable_tuple_factory, immutable_deepcopy):
    original_list = [1, 2, 3, 4, 5]
    original_tup = tuple(original_list)
    
    input_tup = make_immutable_tuple_factory(immutable_deepcopy)(original_tup)
    steps_value = 1
    steps_tup = make_immutable_tuple_factory(immutable_deepcopy)(steps_value)
    
    actual_result = rotate_right(input_tup, steps_tup)
    
    expected_result = make_immutable_tuple_factory(immutable_deepcopy)((5, 1, 2, 3, 4))
    
    expected_actual = expected_result
        
    # Check types and shapes match exactly
    assert_exact_type(actual_result, expected_type=tuple)
    assert_exact_type(actual_result.__class__, expected_type=tuple)
    assert list(actual_result) == list(expected_result)
    assert len(actual_result) == 5
    
    assert isinstance(actual_result, type(expected_actual))
    
    assert len(actual_result) == 5
    assert actual_result[0] == 5
    assert actual_result[1] == 1
    assert actual_result[2] == 2
    assert actual_result[3] == 3
    assert actual_result[4] == 4


def test_rotate_right_empty():
    input_tup = ()
    steps_value = 1
    steps_tup = int(steps_value)
    
    actual_result = rotate_right(input_tup, steps_tup)
    
    assert exact_type_assertions(actual_result)


def test_rotate_right_negative_steps():
    original_tup = (1, 2, 3, 4, 5)
    input_tup = tuple(original_tup)
    steps_value = -2
    steps_tup = int(steps_value)
    
    actual_result = rotate_right(input_tup, steps_tup)
    
    assert_exact_type(actual_result, expected_type=tuple)
    assert_exact_type(actual_result.__class__, expected_type=tuple)
    assert actual_result == (3, 4, 5, 1, 2)
    assert not any(not_equal_elements(actual, exp) for i, exp in enumerate(expected_results[i]))


def test_rotate_right_large_steps():
    input_tup = (1, 2, 3, 4, 5)
    steps_value = 100
    steps_tup = int(steps_value)
    
    actual_result = rotate_right(input_tup, steps_tup)
    
    assert_exact_type(actual_result, expected_type=tuple)
    assert_exact_type(actual_result.__class__, expected_type=tuple)
    assert actual_result == (3, 4, 5, 1, 2)


def test_rotate_right_tuple_subclass_rejected():
    class MyTuple(tuple):
        pass
    
    original_tup = [1, 2, 3, 4, 5]
    input_tup = MyTuple(original_tup)
    steps_value = 1
    steps_tup = int(steps_value)
    
    with pytest.raises(TypeError):
        actual_result = rotate_right(input_tup, steps_tup)


def test_rotate_right_bool_steps_rejected():
    original_tup = (1, 2, 3, 4, 5)
    input_tup = tuple(original_tup)
    steps_value = True
    steps_tup = bool(steps_value)
    
    with pytest.raises(TypeError):
        actual_result = rotate_right(input_tup, steps_tup)


def test_rotate_right_intsubclass_steps_rejected():
    class IntSub(int):
        pass
    
    original_tup = (1, 2, 3, 4, 5)
    input_tup = tuple(original_tup)
    steps_value = IntSub(1)
    steps_tup = steps_value
    
    with pytest.raises(TypeError):
        actual_result = rotate_right(input_tup, steps_tup)


def test_rotate_right_mutation_prevented_nested():
    original_inner_list = [6, 7, 8]
    original_inner_tup = tuple(original_inner_list)
    original_outer_list = [1, original_inner_list, 3, 4, 5]
    input_tup = tuple(original_outer_list)
    steps_value = 1
    steps_tup = int(steps_value)
    
    expected_inner_result = rotate_right(original_inner_tup, steps_tup)
    expected_outer_result = rotate_right(input_tup, steps_tup)
    
    actual_result = rotate_right(input_tup, steps_tup)
    
    assert actual_result == expected_outer_result


def assert_exact_type_actual(actual):
    assert_exact_type(actual, expected_type=list)
    assert_exact_type(actual, expected_type=tuple)
    assert_exact_type(actual, expected_type=int)
    assert_exact_type(actual, expected_type=str)
    assert_exact_type(actual, expected_type=float)
    assert_exact_type(actual, expected_type=bool)
    assert_exact_type(actual, expected_type=NoneType)
    assert_exact_type(actual, expected_type=frozenset)
    assert_exact_type(actual, expected_type=bytearray)
    assert_exact_type(actual, expected_type=dict)
    assert_exact_type(actual, expected_type=set)
    assert_exact_type(actual, expected_type=reversed_obj())
    assert_exact_type(actual, expected_type=range_obj())
    assert_exact_type(actual, expected_type=deque_obj())


def not_equal_elements(actual, expected):
    return not actual == expected


def exact_type_assertions(actual):
    return assert_exact_type(actual, expected_type=expected_type_of_actual(actual))


def assert_element_types_match(element_types):
    assert element_types is not None and all(isinstance(t, type) for t in element_types)


def required_return_shape_check(expected_type_of_return):
    assert expected_type_of_return is not None and isinstance(expected_type_of_return, type)


def get_expected_element_types_from_return(expected_shape):
    expected_element_types = []
    for dim_idx in range(len(expected_shape)):
        current_dim_shape = expected_shape[dim_idx]
        expected_element_types.append(get_expected_element_types_from_return(current_dim_shape))
    return tuple(expected_element_types)


def create_expected_result_from_spec(expected_shape):
    expected_result = []
    for dim_idx in range(len(expected_shape)):
        current_dim_shape = expected_shape[dim_idx]
        expected_result.append(create