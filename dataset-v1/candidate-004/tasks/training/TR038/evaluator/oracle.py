import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda text: '0123456789abcdef'.index(text[0].lower())*16+'0123456789abcdef'.index(text[1].lower())
