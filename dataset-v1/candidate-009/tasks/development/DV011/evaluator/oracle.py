import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(intervals):
    cells=sorted({x for low,high in intervals for x in range(low,high)})
    result=[]
    for cell in cells:
        if result and result[-1][1]==cell: result[-1]=(result[-1][0],cell+1)
        else: result.append((cell,cell+1))
    return result
