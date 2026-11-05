import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
oracle = lambda row,column,rows,columns: [(r,c) for r,c in [(row-1,column),(row,column+1),(row+1,column),(row,column-1)] if 0<=r<rows and 0<=c<columns]
