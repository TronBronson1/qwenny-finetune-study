"""Original local task records. No model outputs or external datasets are used."""
from dataclasses import dataclass, field
import bisect, calendar, collections, csv, datetime, fractions, functools, heapq, html, io, itertools, math, operator, re, statistics, textwrap

TASKS = {}

@dataclass
class Task:
    name: str
    params: tuple
    schemas: tuple
    contract: str
    body: str
    oracle: str
    inputs: list
    invalid: list = field(default_factory=list)  # (args, expected exception)
    extra: list = field(default_factory=list)
    kind: str = "generate-tests"
    bug: str = ""
    rubric: list = field(default_factory=list)
    extra_tests: str = ""
    signature: str = ""
    mutates: bool = False

def add(name, params, schemas, contract, body, oracle, inputs, invalid=(), extra=(), **kwargs):
    assert name not in TASKS
    TASKS[name] = Task(name,tuple(params.split()),tuple(schemas.split()),contract,textwrap.dedent(body).strip(),textwrap.dedent(oracle).strip(),list(inputs),list(invalid),list(extra),**kwargs)

COMMON = '''
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
'''

IMPORTS = {k:v for k,v in globals().copy().items() if k in [
    "bisect","calendar","collections","csv","datetime","fractions","functools",
    "heapq","html","io","itertools","math","operator","re","statistics","textwrap"]}

def source(task):
    args=task.signature or ", ".join(task.params)
    values="("+", ".join(task.params)+("," if len(task.params)==1 else "")+")"
    code=f"def {task.name}({args}):\n    _types({values}, {task.schemas!r})\n"
    return COMMON+"\n"+code+textwrap.indent(task.body,"    ")+"\n"

def oracle_function(task):
    namespace=dict(IMPORTS)
    if task.oracle.startswith("lambda"):
        return eval(task.oracle,namespace)
    exec(task.oracle,namespace)
    return namespace["oracle"]
