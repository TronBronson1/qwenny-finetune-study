def oracle(values,steps):
    queue=collections.deque(values)
    queue.rotate(steps)
    return tuple(queue)
