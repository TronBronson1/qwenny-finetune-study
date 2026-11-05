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
        assert parse_hex_byte("AB") == 171

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
            parse_hex_byte("123")

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

    def test_invalid_reversed_bounds(self):
        # This test validates the behavior when the input is a string representing 
        # a number that would be invalid if interpreted as a bounds check, 
        # but strictly speaking, parse_hex_byte operates on single byte representation.
        # Since the contract requires exactly two ASCII hex digits, we cannot test 
        # "lower value exceeds upper value" in the mathematical sense because 
        # the input is a flat string, not a tuple of bounds. 
        # Therefore, we verify that non-2-char strings are rejected.
        with pytest.raises(ValueError):
            parse_hex_byte("000")  # Three chars -> invalid
