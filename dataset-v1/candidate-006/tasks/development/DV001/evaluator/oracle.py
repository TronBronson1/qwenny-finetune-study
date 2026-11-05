import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(values,steps):
    queue=collections.deque(values)
    queue.rotate(steps)
    return tuple(queue)
