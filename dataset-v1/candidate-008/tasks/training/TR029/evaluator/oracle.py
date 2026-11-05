import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(values,width):
    result=[]
    current=[]
    for item in values:
        current.append(item)
        if len(current)==width: result.append(current); current=[]
    if current: result.append(current)
    return result
