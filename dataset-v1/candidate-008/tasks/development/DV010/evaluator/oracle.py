import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(tokens):
    def parse(index):
        token=tokens[index]
        if token not in ("+","-","*"): return int(token),index-1
        right,index=parse(index-1)
        left,index=parse(index)
        return {"+":lambda:left+right,"-":lambda:left-right,"*":lambda:left*right}[token](),index
    value,index=parse(len(tokens)-1)
    assert index==-1
    return value
