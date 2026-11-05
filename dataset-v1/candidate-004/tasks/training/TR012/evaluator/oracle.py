import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda day,delta: (datetime.date(2001,1,1)+datetime.timedelta(days=day+delta)).weekday()
