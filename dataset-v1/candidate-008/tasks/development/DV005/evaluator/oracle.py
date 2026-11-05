import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda text: max([0]+[text[:i].count('(')-text[:i].count(')') for i in range(1,len(text)+1)])
