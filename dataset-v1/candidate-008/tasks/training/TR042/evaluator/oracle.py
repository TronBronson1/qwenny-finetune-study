import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda text: tuple(sum((ord(c)-48)*10**i for i,c in enumerate(reversed(p))) for p in text.split('.'))
