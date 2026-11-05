def clamp_integer(value, lower, upper):
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    if any(type(item) is not int for item in (value, lower, upper)):
        raise TypeError("all arguments must be exact built-in integers")
    return min(max(value, lower), upper)
