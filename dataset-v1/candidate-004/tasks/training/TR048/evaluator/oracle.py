import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(number):
    if number<=26: return chr(64+number)
    if number<=702:
        n=number-27
        return chr(65+n//26)+chr(65+n%26)
    n=number-703
    return chr(65+n//676)+chr(65+(n//26)%26)+chr(65+n%26)
