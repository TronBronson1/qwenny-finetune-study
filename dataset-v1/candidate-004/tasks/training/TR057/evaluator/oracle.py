import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(text):
    words=[]
    current=""
    for char in text:
        if char in " _-":
            if current: words.append(current); current=""
        else: current+=char.lower()
    if current: words.append(current)
    return "-".join(words)
