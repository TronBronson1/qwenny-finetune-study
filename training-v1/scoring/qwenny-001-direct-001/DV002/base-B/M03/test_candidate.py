from subject import minute_of_day

class StrSub(str):
    pass

class IntSub(int):
    pass

# Valid inputs covering edge hours (0, 23), edge minutes (0, 59), and middle values
@pytest.mark.parametrize("text,expected", [
    ("00:00", 0),          # Min hour/min
    ("23:59", 1439),       # Max hour/min
    ("05:03", 303),        # Middle values
    ("12:30", 750),        # Noon/teens
])
def test_valid_ascii_time(text, expected):
    result = minute_of_day(text)
    assert isinstance(result, int)
    assert result == expected

# Invalid types for 'text' (built-in str required)
@pytest.mark.parametrize("text", [
    StrSub("12:30"),
    "12:30" if isinstance("12:30", type("X")) else None  # Fallback logic not needed if we just pass a subclass instance; but here we need an actual subclass instance. 
])
def test_invalid_type_str_subclass():
    invalid_text = StrSub("12:30")
    with pytest.raises(TypeError):
        minute_of_day(invalid_text)

# Additional explicit invalid type case using a dynamic subclass to ensure coverage of subclasses generally
type_DynStr = type('DynStr', (str,), {})
test_cases_invalid_type_dyn = []
for bad_val in ["12:30"]:
    test_cases_invalid_type_dyn.append(DynStr(bad_val))
    
@pytest.mark.parametrize("text", test_cases_invalid_type_dyn)
def test_invalid_type_dynamic_str(text):
    with pytest.raises(TypeError):
        minute_of_day(text)


# Invalid string formats (shape/value checks leading to ValueError)
@pytest.mark.parametrize("text", [
    "12:60",              # Minute out of range
    "24:00",              # Hour out of range
    "12:6",               # Wrong format (minutes single digit)
    "1-30",               # Wrong separator
    "000:00",             # Too many characters
    "00:0",               # Too few characters
    "abc:de",             # Non-numeric
    "",                   # Empty
    "12",                 # Missing colon
    "12:30:00",           # Extra part
    "12:",                # Trailing colon
    ":30",                # Leading colon
    "-1:00",              # Negative hour
    "12:-30",             # Negative minute
    "00:60",              # Invalid minute (60)
])
def test_invalid_format_raises_error(text):
    with pytest.raises(ValueError):
        minute_of_day(text)
