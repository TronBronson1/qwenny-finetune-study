import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda text,needle,occurrence: ([i for i in range(len(text)) if text.startswith(needle,i)]+[-1]*occurrence)[occurrence-1]
