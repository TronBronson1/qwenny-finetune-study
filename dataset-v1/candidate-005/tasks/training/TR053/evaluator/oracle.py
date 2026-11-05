import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(cents):
    digits=str(abs(cents)).zfill(3)
    return ("-" if cents<0 else "")+digits[:-2]+"."+digits[-2:]
