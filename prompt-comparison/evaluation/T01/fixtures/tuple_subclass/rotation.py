def rotate_right(values, steps):
    if not isinstance(values, tuple) or type(steps) is not int:
        raise TypeError
    if not values:
        return ()
    k = steps % len(values)
    return values[-k:] + values[:-k] if k else values[:]
