import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(left,right):
    pool=list(right)
    result=[]
    for value in left:
        if value in pool:
            result.append(value); pool.remove(value)
    return result
