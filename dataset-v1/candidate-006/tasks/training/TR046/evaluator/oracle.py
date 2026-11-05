import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(text):
    sign=-1 if text.startswith("-") else 1
    digits=text[1:] if text[:1] in ("+","-") else text
    result=0
    for char in digits: result=result*10+ord(char)-48
    return sign*result
