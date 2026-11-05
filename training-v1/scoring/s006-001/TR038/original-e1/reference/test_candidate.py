from subject import parse_hex_byte
import pytest


class TestParseHexByte:
    def test_valid_hex_0(self):
        assert parse_hex_byte("00") == 0

    def test_valid_hex_1(self):
        assert parse_hex_byte("01") == 1

    def test_valid_hex_f(self):
        assert parse_hex_byte("ff") == 255

    def test_valid_hex_uppercase(self):
        assert parse_hex_byte("AA") == 170

    def test_valid_hex_mixed_case(self):
        assert parse_hex_byte("aB") == 171

    def test_invalid_non_hex_char(self):
        with pytest.raises(ValueError):
            parse_hex_byte("1G")

    def test_invalid_single_char(self):
        with pytest.raises(ValueError):
            parse_hex_byte("1")

    def test_invalid_three_chars(self):
        with pytest.raises(ValueError):
            parse_hex_byte("000")

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError):
            parse_hex_byte("")

    def test_invalid_type_string_subclass(self):
        class MyStr(str):
            pass
        with pytest.raises(TypeError):
            parse_hex_byte(MyStr("00"))

    def test_invalid_type_integer(self):
        with pytest.raises(TypeError):
            parse_hex_byte(0)

    def test_invalid_type_bytes(self):
        with pytest.raises(TypeError):
            parse_hex_byte(b"00")

    def test_invalid_type_none(self):
        with pytest.raises(TypeError):
            parse_hex_byte(None)

    def test_invalid_type_float(self):
        with pytest.raises(TypeError):
            parse_hex_byte(0.0)

    def test_invalid_type_list(self):
        with pytest.raises(TypeError):
            parse_hex_byte(["00"])

    def test_invalid_type_dict(self):
        with pytest.raises(TypeError):
            parse_hex_byte({"00": "00"})


# Limitations:
# 1. This file defines parametrized tests with explicit argument tuples; it does not generate 
#    all possible combinations (e.g., all 66 valid hex byte strings are not explicitly tested).
# 2. While type checks for str subclasses and common non-str types are covered, exhaustive 
#    coverage of every object type is not guaranteed.
# 3. Reversed-bounds logic is not applicable here since the input is a fixed-length string 
#    rather than numeric bounds; the ValueError test for non-hex chars covers length validation.
# 4. Mutation checking is not verified via test assertions; it relies on the function contract.
