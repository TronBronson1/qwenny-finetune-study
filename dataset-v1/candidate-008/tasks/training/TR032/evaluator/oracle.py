import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(values):
    groups={-1:[],0:[],1:[]}
    for x in values: groups[(x>0)-(x<0)].append(x)
    return groups[-1],groups[0],groups[1]
