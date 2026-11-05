
import math, re, collections, itertools, calendar, datetime, bisect, heapq, fractions, csv, io, html, statistics, operator, types

def _exact(value, kind):
    if type(value) is not kind:
        raise TypeError("exact built-in type required")

def _check(value, schema):
    if schema in ("int", "str", "bytes"):
        _exact(value, {"int": int, "str": str, "bytes": bytes}[schema])
    elif schema in ("ints", "strs", "matrix", "pairs", "commands"):
        _exact(value, list)
        for item in value:
            if schema == "ints": _exact(item, int)
            elif schema == "strs": _exact(item, str)
            elif schema == "matrix": _check(item, "ints")
            elif schema == "pairs": _check(item, "pair")
            elif schema == "commands": _exact(item, tuple)
    elif schema in ("pair", "tuple3"):
        _exact(value, tuple)
        for item in value: _exact(item, int)
    elif schema == "objects":
        _exact(value, tuple)
    elif schema == "maybe_strs":
        if value is not None: _check(value, "strs")
    elif schema == "stream":
        if type(value) not in (list, tuple, types.GeneratorType): raise TypeError("iterable kind")
    elif schema in ("counts", "aliases"):
        _exact(value, dict)
        for key, item in value.items():
            _exact(key, str)
            _exact(item, int if schema == "counts" else str)
    else:
        raise AssertionError(schema)

def _types(values, schemas):
    for value, schema in zip(values, schemas): _check(value, schema)
    # Shape/value validation happens after every argument's nested type validation.
    for value, schema in zip(values, schemas):
        if schema in ("pair", "tuple3") and len(value) != (2 if schema == "pair" else 3):
            raise ValueError("tuple shape")
        if schema == "pairs" and any(len(item) != 2 for item in value):
            raise ValueError("pair shape")

def interval_union(intervals):
    _types((intervals,), ('pairs',))
    if any(low>=high for low,high in intervals): raise ValueError("interval")
    result=[]
    for low,high in sorted(intervals):
        if result and low<=result[-1][1]: result[-1]=(result[-1][0],max(high,result[-1][1]))
        else: result.append((low,high))
    return result

# --- independent-review mutant: value/shape checks before type checks ---
_mut_orig = interval_union
_MUT_SCHEMAS = ('pairs',)
_MUT_BASE = ([],)
def _mut_valid(value, schema):
    try:
        _check(value, schema)
        return True
    except TypeError:
        return False
def _mut_repair(value, schema, base):
    # Replace type-invalid nested items by a valid neighbour (models a per-item
    # value check that runs before the remaining type checks).
    sub = {"ints": "int", "strs": "str", "matrix": "ints", "pairs": "pair"}.get(schema)
    if sub is None or type(value) is not list:
        return base
    fallback = base[0] if base else {"int": 0, "str": "a", "ints": [], "pair": (0, 1)}[sub]
    out, last = [], None
    good = [item for item in value if _mut_valid(item, sub)]
    for item in value:
        if _mut_valid(item, sub):
            out.append(item); last = item
        else:
            out.append(last if last is not None else (good[0] if good else fallback))
    return out
def interval_union(*args):
    try:
        return _mut_orig(*args)
    except TypeError as first:
        fixed = list(args)
        for index, (value, schema) in enumerate(zip(args, _MUT_SCHEMAS)):
            if not _mut_valid(value, schema):
                fixed[index] = _mut_repair(value, schema, _MUT_BASE[index])
        try:
            _mut_orig(*fixed)
        except (ValueError, IndexError) as later:
            raise type(later)(str(later)) from None
        except TypeError:
            pass
        raise first
