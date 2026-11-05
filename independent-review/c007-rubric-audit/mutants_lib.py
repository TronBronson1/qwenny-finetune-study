"""Rubric-mutant generation for the dataset-v1 training/development tasks.

Every mutant is the unchanged reference source with one appended override that
violates exactly one stated requirement. Nothing in the repository is modified.
"""
import io
import json
import re
import tokenize
from pathlib import Path

LIST_SCHEMAS = ("ints", "strs", "matrix", "pairs")

# Schema -> list of (level, kind) checked by the reference _check().
LEVELS = {
    "int": [(0, "int")],
    "str": [(0, "str")],
    "ints": [(0, "list"), (1, "int")],
    "strs": [(0, "list"), (1, "str")],
    "matrix": [(0, "list"), (1, "list"), (2, "int")],
    "pairs": [(0, "list"), (1, "tuple"), (2, "int")],
    "tuple3": [(0, "tuple"), (1, "int")],
    "pair": [(0, "tuple"), (1, "int")],
    "objects": [(0, "tuple")],
}

# Requirement families (stable identifiers used in JSON and REPORT.md).
FAMILY = {
    "type-subclass": "exact types: subclass rejected",
    "type-bool": "exact types: bool rejected where int required",
    "type-ordinary": "exact types: ordinary wrong type rejected",
    "return-subclass": "exact return types: subclass returned",
    "return-swap": "exact return types: ordinary wrong type returned",
    "order": "type-before-value validation order",
    "exception-class": "correct exception class",
    "mutation-valid": "no input mutation (valid calls)",
    "mutation-error": "no input mutation (error path; contract-only)",
    "ascii": "ASCII-only rule",
    "case": "case-sensitivity / stated letter case",
    "boundary": "boundary off-by-one",
}


def parse_reference(source):
    match = re.search(r"\ndef (\w+)\(([^)]*)\):\n    _types\(\((.*?)\), \((.*?)\)\)", source)
    if not match:
        raise ValueError("reference shape not recognised")
    name, params, _, schemas = match.groups()
    schemas = tuple(s.strip().strip("'") for s in schemas.split(",") if s.strip())
    params = tuple(p.strip() for p in params.split(","))
    body_start = match.start() + 1
    return {"name": name, "params": params, "schemas": schemas, "body_start": body_start}


# ---------------------------------------------------------------------------
# Override snippets.  Each one is appended to the reference source.

TYPE_OVERRIDE = '''
# --- independent-review mutant: relax ONE exact-type check -----------------
_MUT_TARGET = {target!r}
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
        _mut_exact(value, {{"int": int, "str": str, "bytes": bytes}}[schema], here)
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
'''

WRAP_HEAD = '''
# --- independent-review mutant: {label} ---
_mut_orig = {name}
_MUT_SCHEMAS = {schemas!r}
'''

ORDER_OVERRIDE = WRAP_HEAD + '''_MUT_BASE = {base}
def _mut_valid(value, schema):
    try:
        _check(value, schema)
        return True
    except TypeError:
        return False
def _mut_repair(value, schema, base):
    # Replace type-invalid nested items by a valid neighbour (models a per-item
    # value check that runs before the remaining type checks).
    sub = {{"ints": "int", "strs": "str", "matrix": "ints", "pairs": "pair"}}.get(schema)
    if sub is None or type(value) is not list:
        return base
    fallback = base[0] if base else {{"int": 0, "str": "a", "ints": [], "pair": (0, 1)}}[sub]
    out, last = [], None
    good = [item for item in value if _mut_valid(item, sub)]
    for item in value:
        if _mut_valid(item, sub):
            out.append(item); last = item
        else:
            out.append(last if last is not None else (good[0] if good else fallback))
    return out
def {name}(*args):
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
'''

EXC_OVERRIDE = WRAP_HEAD + '''def {name}(*args):
    try:
        return _mut_orig(*args)
    except {src} as error:
        if type(error) is not {src}: raise
        raise {dst}(str(error)) from None
'''

MUTATE_VALID_OVERRIDE = WRAP_HEAD + '''def {name}(*args):
    result = _mut_orig(*args)
    target = args[{pos}]
    {action}
    return result
'''

MUTATE_ERROR_OVERRIDE = WRAP_HEAD + '''def {name}(*args):
    try:
        return _mut_orig(*args)
    except Exception:
        target = args[{pos}]
        if isinstance(target, list):
            target.append(target[-1] if target else {filler!r})
        raise
'''

RETURN_OVERRIDE = WRAP_HEAD + '''class _RetInt(int): pass
class _RetStr(str): pass
class _RetList(list): pass
class _RetTuple(tuple): pass
def _mut_retype(value, depth, mode):
    if depth > 0:
        if type(value) in (list, tuple):
            return type(value)(_mut_retype(item, depth - 1, mode) for item in value)
        return value
    kind = type(value)
    if mode == "subclass":
        table = {{int: _RetInt, str: _RetStr, list: _RetList, tuple: _RetTuple}}
        return table[kind](value) if kind in table else value
    if kind is list: return tuple(value)
    if kind is tuple: return list(value)
    if kind is bool: return int(value)
    return value
def {name}(*args):
    return _mut_retype(_mut_orig(*args), {depth}, {mode!r})
'''

STRMAP_OVERRIDE = WRAP_HEAD + '''import unicodedata as _mut_ud
def _mut_map_text(text):
    {mapper}
def _mut_map(value, schema):
    if schema == "str" and type(value) is str: return _mut_map_text(value)
    if schema == "strs" and type(value) is list and all(type(item) is str for item in value):
        return [_mut_map_text(item) for item in value]
    return value
def {name}(*args):
    return _mut_orig(*(_mut_map(value, schema) for value, schema in zip(args, _MUT_SCHEMAS)))
'''

OUTCASE_OVERRIDE = WRAP_HEAD + '''def {name}(*args):
    result = _mut_orig(*args)
    return result.{method}() if type(result) is str else result
'''

STRMAPPERS = {
    "unicode-decimal-digits": "return ''.join(str(_mut_ud.decimal(c)) if not c.isascii() and _mut_ud.decimal(c, None) is not None else c for c in text)",
    "nfkc-normalize": "return _mut_ud.normalize('NFKC', text)",
    "fold-lower": "return text.lower()",
    "fold-upper": "return text.upper()",
}

# Unicode-aware replacements of ASCII-only predicates (applied to the function body).
ASCII_TEXTUAL = [
    ('"A" <= char <= "Z" or "a" <= char <= "z"', "char.isalpha()"),
    ('"0" <= char <= "9"', "char.isdigit()"),
    ('"a" <= char <= "z"', "char.islower()"),
    ('not "A" <= char <= "Z"', "not char.isupper()"),
    ('[0-9]', r'\d'),
    ('char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_"',
     'not (char.isalnum() or char in " -_")'),
    ('char != " "', "not char.isspace()"),
]

# Task-specific single-requirement mutants where the generic families cannot express the rule.
SPECIFIC = {
    "TR015": [("unicode-whitespace", "ascii",
               "' '.join(reversed(text.split()))", "' '.join(reversed([w for w in text.split(' ') if w]))")],
}


def body_tokens(body):
    return list(tokenize.generate_tokens(io.StringIO(body).readline))


def boundary_variants(body):
    """Single-site comparison-operator and literal off-by-one variants of the function body."""
    lines = body.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    def absolute(position):
        row, col = position
        return offsets[row - 1] + col
    flips = {"<": "<=", "<=": "<", ">": ">=", ">=": ">"}
    out = []
    for tok in body_tokens(body):
        start, end = absolute(tok.start), absolute(tok.end)
        line = tok.line
        if tok.start[0] <= 2:  # def line and the _types(...) call
            continue
        if tok.type == tokenize.OP and tok.string in flips:
            new = body[:start] + flips[tok.string] + body[end:]
            out.append((f"op{tok.start[0]}:{tok.start[1]}:{tok.string}->{flips[tok.string]}", new))
        elif tok.type == tokenize.NUMBER and re.search(r"<|>|range\(|len\(", line) and tok.string.isdigit():
            value = int(tok.string)
            for delta in (-1, 1):
                if value + delta < 0:
                    continue
                new = body[:start] + str(value + delta) + body[end:]
                out.append((f"num{tok.start[0]}:{tok.start[1]}:{value}->{value + delta}", new))
        elif tok.type == tokenize.STRING:
            for quant in re.finditer(r"\{(\d+)(?:,(\d+))?\}", tok.string):
                for group in (1, 2):
                    if quant.group(group) is None:
                        continue
                    value = int(quant.group(group))
                    for delta in (-1, 1):
                        nv = value + delta
                        lo = int(quant.group(1)); hi = int(quant.group(2)) if quant.group(2) else lo
                        lo2, hi2 = (nv, hi) if group == 1 else (lo, nv)
                        if nv < 0 or (quant.group(2) is not None and lo2 > hi2):
                            continue
                        s, e = quant.span(group)
                        text = tok.string[:s] + str(nv) + tok.string[e:]
                        if quant.group(2) is None:
                            text = tok.string[:quant.start()] + "{" + str(nv) + "}" + tok.string[quant.end():]
                        new = body[:start] + text + body[end:]
                        out.append((f"re{tok.start[0]}:{quant.group(0)}:{group}:{value}->{nv}", new))
    seen, unique = set(), []
    for key, new in out:
        if new not in seen and new != body:
            seen.add(new)
            unique.append((key, new))
    return unique


def spec_flags(spec):
    lower = spec.lower()
    contract = lower.split("coverage expectations")[0]
    return {
        "ascii": "ascii" in contract or "unicode digits" in contract,
        "case_input": any(k in contract for k in ("case-sensitive", "case-sensitively", "in lowercase", "uppercase ascii", "case-insensitive")),
        "case_output": any(k in contract for k in ("lowercase positional", "lowercase hexadecimal", "uppercase roman", "lowercase letters", "uppercase only")),
    }


def build_mutants(task_id, source, spec, base_args, raised_classes, return_depth):
    """Return a list of mutant dicts: id, family, requirement, override, source."""
    info = parse_reference(source)
    name, schemas = info["name"], info["schemas"]
    flags = spec_flags(spec)
    mutants = []

    def add(mid, family, requirement, src, override):
        mutants.append({"id": mid, "family": family, "requirement": requirement,
                        "override": override, "source": src})

    def wrap(template, label, **kw):
        override = template.format(label=label, name=name, schemas=schemas, **kw)
        return source + override, override

    # 1. exact input types: every position and stated level.
    for pos, schema in enumerate(schemas):
        for level, kind in LEVELS[schema]:
            modes = ["subclass", "ordinary"] + (["bool"] if kind == "int" else [])
            for mode in modes:
                family = {"subclass": "type-subclass", "ordinary": "type-ordinary", "bool": "type-bool"}[mode]
                override = TYPE_OVERRIDE.format(target=(pos, level, mode))
                add(f"T-{info['params'][pos]}-L{level}-{mode}", family,
                    f"{info['params'][pos]} level {level} ({kind}): {FAMILY[family]}", source + override, override)

    # 2. exact return types at each observed level.
    for depth in range(return_depth + 1):
        for mode, family in (("subclass", "return-subclass"), ("swap", "return-swap")):
            src, override = wrap(RETURN_OVERRIDE, f"return level {depth} {mode}", depth=depth, mode=mode)
            add(f"R-L{depth}-{mode}", family, f"return level {depth}: {FAMILY[family]}", src, override)

    # 3. validation order: value/shape checks before type checks.
    base_src = "(" + ", ".join(base_args) + ("," if len(base_args) == 1 else "") + ")"
    src, override = wrap(ORDER_OVERRIDE, "value/shape checks before type checks", base=base_src)
    add("O-value-before-type", "order", FAMILY["order"], src, override)

    # 4. exception classes.
    swaps = {"TypeError": ["ValueError"], "ValueError": ["TypeError", "IndexError"], "IndexError": ["ValueError"]}
    for cls in sorted(raised_classes):
        for dst in swaps.get(cls, []):
            if dst == "IndexError" and "IndexError" not in raised_classes:
                continue
            src, override = wrap(EXC_OVERRIDE, f"{cls} raised as {dst}", src=cls, dst=dst)
            add(f"E-{cls}-as-{dst}", "exception-class", f"{cls} must not become {dst}", src, override)

    # 5. input mutation.
    for pos, schema in enumerate(schemas):
        param = info["params"][pos]
        filler = {"ints": 0, "strs": "", "matrix": [], "pairs": (0, 1)}.get(schema)
        if schema in LIST_SCHEMAS:
            actions = {
                "append": f"target.append(target[-1] if target else {filler!r})",
                "sort": "target.sort()",
            }
            if schema == "matrix":
                actions["nested-append"] = "[row.append(0) for row in target]"
            for key, action in actions.items():
                src, override = wrap(MUTATE_VALID_OVERRIDE, f"mutate {param} ({key})", pos=pos, action=action)
                add(f"M-{param}-{key}", "mutation-valid", f"{param}: {FAMILY['mutation-valid']} ({key})", src, override)
            src, override = wrap(MUTATE_ERROR_OVERRIDE, f"mutate {param} before raising", pos=pos, filler=filler)
            add(f"M-{param}-on-error", "mutation-error", f"{param}: {FAMILY['mutation-error']}", src, override)
        if schema == "objects":
            action = "[item.append(0) for item in target if type(item) is list]"
            src, override = wrap(MUTATE_VALID_OVERRIDE, f"mutate nested elements of {param}", pos=pos, action=action)
            add(f"M-{param}-nested-elements", "mutation-valid", f"{param}: {FAMILY['mutation-valid']} (nested elements)", src, override)

    has_text = any(s in ("str", "strs") for s in schemas)
    body = source[info["body_start"]:]
    # 6. ASCII-only rules.
    if has_text and flags["ascii"]:
        for key in ("unicode-decimal-digits", "nfkc-normalize"):
            src, override = wrap(STRMAP_OVERRIDE, f"ASCII rule violated: {key}", mapper=STRMAPPERS[key])
            add(f"A-{key}", "ascii", f"{FAMILY['ascii']}: {key}", src, override)
        for index, (old, new) in enumerate(ASCII_TEXTUAL):
            if old in body:
                changed = body.replace(old, new)
                add(f"A-predicate-{index}", "ascii", f"{FAMILY['ascii']}: '{old}' -> '{new}'",
                    source[:info["body_start"]] + changed, f"body: {old!r} -> {new!r}")
    for mid, family, old, new in SPECIFIC.get(task_id, []):
        if old in body:
            add(f"S-{mid}", family, f"{FAMILY[family]}: {mid}",
                source[:info["body_start"]] + body.replace(old, new), f"body: {old!r} -> {new!r}")
    # 7. case rules.
    if has_text and flags["case_input"]:
        for key in ("fold-lower", "fold-upper"):
            src, override = wrap(STRMAP_OVERRIDE, f"case rule violated: {key}", mapper=STRMAPPERS[key])
            add(f"C-input-{key}", "case", f"{FAMILY['case']}: input {key}", src, override)
    if flags["case_output"]:
        for method in ("upper", "lower"):
            src, override = wrap(OUTCASE_OVERRIDE, f"output case {method}", method=method)
            add(f"C-output-{method}", "case", f"{FAMILY['case']}: output {method}()", src, override)
    # 8. boundary off-by-ones.
    for key, new_body in boundary_variants(body):
        add(f"B-{key}", "boundary", f"{FAMILY['boundary']}: {key}",
            source[:info["body_start"]] + new_body, f"body edit {key}")
    return info, mutants
