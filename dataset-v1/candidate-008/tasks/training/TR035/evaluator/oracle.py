import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda values: sum(max(0,len(list(g))-1) for _,g in itertools.groupby(values))
