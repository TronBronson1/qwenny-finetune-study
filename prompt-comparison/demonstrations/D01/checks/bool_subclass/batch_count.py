def batches(items, capacity):
    if not isinstance(items, int) or not isinstance(capacity, int):
        raise TypeError
    if items < 0 or capacity <= 0:
        raise ValueError
    return (items + capacity - 1) // capacity
