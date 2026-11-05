import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(left,right):
    for a,b in zip(left,right):
        if a<b: return -1
        if a>b: return 1
    return 0
