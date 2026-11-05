import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda left,right: next((left[:i] for i in range(min(len(left),len(right)),-1,-1) if left[:i]==right[:i]),'')
