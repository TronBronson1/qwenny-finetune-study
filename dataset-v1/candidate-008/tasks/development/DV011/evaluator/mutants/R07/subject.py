
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

# --- independent-review mutant: relax ONE exact-type check -----------------
_MUT_TARGET = (0, 0, 'ordinary')
def _mut_ok(value, kind, path):
    if path == _MUT_TARGET[:2]:
        mode = _MUT_TARGET[2]
        if mode == "ordinary": return type(value) is kind or not isinstance(value, kind)
        if mode == "subclass": return isinstance(value, kind) and type(value) is not bool
        if mode == "bool": return type(value) is kind or type(value) is bool
    return type(value) is kind
def _mut_exact(value, kind, path):
    if not _mut_ok(value, kind, path):
        raise TypeError("exact built-in type required")
def _mut_check(value, schema, pos, level):
    here = (pos, level)
    if schema in ("int", "str", "bytes"):
        _mut_exact(value, {"int": int, "str": str, "bytes": bytes}[schema], here)
    elif schema in ("ints", "strs", "matrix", "pairs", "commands"):
        _mut_exact(value, list, here)
        for item in value:
            if schema == "ints": _mut_exact(item, int, (pos, level + 1))
            elif schema == "strs": _mut_exact(item, str, (pos, level + 1))
            elif schema == "matrix": _mut_check(item, "ints", pos, level + 1)
            elif schema == "pairs": _mut_check(item, "pair", pos, level + 1)
            elif schema == "commands": _mut_exact(item, tuple, (pos, level + 1))
    elif schema in ("pair", "tuple3"):
        _mut_exact(value, tuple, here)
        for item in value: _mut_exact(item, int, (pos, level + 1))
    elif schema == "objects":
        _mut_exact(value, tuple, here)
    else:
        raise AssertionError(schema)
def _types(values, schemas):
    for pos, (value, schema) in enumerate(zip(values, schemas)): _mut_check(value, schema, pos, 0)
    for value, schema in zip(values, schemas):
        if schema in ("pair", "tuple3") and len(value) != (2 if schema == "pair" else 3):
            raise ValueError("tuple shape")
        if schema == "pairs" and any(len(item) != 2 for item in value):
            raise ValueError("pair shape")
