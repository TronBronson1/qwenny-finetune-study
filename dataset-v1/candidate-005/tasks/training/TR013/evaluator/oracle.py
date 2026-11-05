import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(number,base):
    if number == 0: return "0"
    power=1
    while power*base <= number: power*=base
    digits=[]
    while power:
        digit=number//power
        digits.append("0123456789abcdef"[digit])
        number-=digit*power
        power//=base
    return "".join(digits)
