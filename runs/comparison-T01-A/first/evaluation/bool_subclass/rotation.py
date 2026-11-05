def rotate_right(values, steps):
    if type(values) is not tuple or not isinstance(steps, int):
        raise TypeError
    if not values:
        return ()
    k = steps % len(values)
    return values[-k:] + values[:-k] if k else values[:]
