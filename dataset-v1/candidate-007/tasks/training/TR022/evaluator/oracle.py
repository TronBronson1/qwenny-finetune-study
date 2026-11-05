import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, functools, textwrap

# Valid-domain oracle only; rejection cases are specified separately.
def oracle(text):
    stream=io.StringIO(newline="")
    csv.writer(stream,lineterminator="\r\n").writerow([text])
    return stream.getvalue()[:-2]
