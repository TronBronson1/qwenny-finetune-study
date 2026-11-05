from subject import ascii_upper
import pytest

@pytest.mark.parametrize("test_input,expected", [
    ("abc", "ABC"),
    ("AbCd", "ABcD"),
    ("", ""),
    ("hello 世界", "HELLO 世界"),
    ("123!@#", "123!@#"),
    ("A", "A"),
    ("z", "Z"),
    ("a", "A"),
    ("ABC", "ABC"),
    ("!aBc", "!ABC"),
    ("  hello  world  ", "  HELLO  WORLD  "),
    ("日本語", "日本語"),
    ("你好", "你好"),
    ("안녕하세요", "안녕하세요"),
])
def test_ascii_upper_returns_correct_str(test_input, expected):
    assert isinstance(test_input, str)
    result = ascii_upper(test_input)
    assert isinstance(result, str)
    assert result == expected
    assert result is not test_input

@pytest.mark.parametrize("test_input", [
    123,
    12.5,
    True,
    None,
    [],
    {},
    ("a",),
    [1, 2, 3],
    {1: 2},
    {"a": "b"},
    lambda x: x,
    bytearray(b"abc"),
    "ab" + str(type(str)),  # Invalid type injection attempt simulation
])
def test_ascii_upper_raises_type_error(test_input):
    with pytest.raises(TypeError):
        ascii_upper(test_input)

@pytest.mark.parametrize("test_input", [
    {"a": "b"},
    [1, 2, 3],
    {"nested": "value"},
    {"list": ["x", "y"]},
    {"mixed": "123"},
    {"list": ["a", "B", "c"]},
    {"str": "Hello", "int": 10},
])
def test_ascii_upper_does_not_mutate_nested(test_input):
    import copy
    original = copy.deepcopy(test_input)
    ascii_upper(test_input)
    assert test_input is original, "Nested structures must not be mutated"

@pytest.mark.parametrize("test_input", [
    "abc",
    "Hello",
    "123",
    "!",
    "",
    "a",
    "Z",
    "1",
    "aB",
    "abc123",
])
def test_ascii_upper_returns_same_object_when_input_is_ascii_uppercase(test_input):
    assert ascii_upper(test_input) is test_input, "Input must be returned as-is if fully uppercase"
