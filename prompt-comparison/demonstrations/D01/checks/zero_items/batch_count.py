def batches(items, capacity):
    if type(items) is not int or type(capacity) is not int:
        raise TypeError
    if items <= 0 or capacity <= 0:
        raise ValueError
    return (items + capacity - 1) // capacity
