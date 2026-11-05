import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(text):
    previous=None
    while previous!=text:
        previous=text
        for pair in ("()","[]","{}"): text=text.replace(pair,"")
    return text==""
