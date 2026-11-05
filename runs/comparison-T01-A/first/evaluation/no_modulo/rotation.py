def rotate_right(values, steps):
    if type(values) is not tuple or type(steps) is not int:
        raise TypeError
    if not values:
        return ()
    k = steps
    return values[-k:] + values[:-k] if k else values[:]
