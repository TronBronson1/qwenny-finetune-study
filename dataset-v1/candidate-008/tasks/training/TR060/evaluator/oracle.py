import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda text: (len(re.findall('[A-Za-z]',text)),len(re.findall('[0-9]',text)),len(re.findall('[^A-Za-z0-9]',text)))
