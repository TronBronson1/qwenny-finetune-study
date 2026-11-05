"""Deterministic probe inputs and outcome comparison for witness search."""
import copy
import io
import random
import re
import signal
import tokenize


class IntChild(int): pass
class StrChild(str): pass
class ListChild(list): pass
class TupleChild(tuple): pass

NAMESPACE = {"IntChild": IntChild, "StrChild": StrChild, "ListChild": ListChild, "TupleChild": TupleChild}


def pyrepr(value):
    """Round-trippable repr that keeps subclass names."""
    kind = type(value)
    if kind in (IntChild, StrChild):
        return f"{kind.__name__}({pyrepr(kind.__mro__[1](value))})"
    if kind is ListChild:
        return f"ListChild([{', '.join(pyrepr(v) for v in value)}])"
    if kind is TupleChild:
        return f"TupleChild({args_repr(tuple(value))})"
    if kind is list:
        return "[" + ", ".join(pyrepr(v) for v in value) + "]"
    if kind is tuple:
        return args_repr(value)
    if kind is dict:
        return "{" + ", ".join(f"{pyrepr(k)}: {pyrepr(v)}" for k, v in value.items()) + "}"
    return repr(value)


def args_repr(args):
    if len(args) == 1:
        return "(" + pyrepr(args[0]) + ",)"
    return "(" + ", ".join(pyrepr(a) for a in args) + ")"


def canon(value, depth=0):
    if depth > 6:
        return ("deep",)
    kind = type(value)
    if isinstance(value, (list, tuple)):
        return (kind.__name__, tuple(canon(v, depth + 1) for v in value))
    if isinstance(value, dict):
        return (kind.__name__, tuple(sorted((repr(k), canon(v, depth + 1)) for k, v in value.items())))
    if kind is object:
        return ("object", id(value))
    return (kind.__name__, repr(value))


class CallTimeout(BaseException):
    pass


def _alarm(signum, frame):
    raise CallTimeout()


signal.signal(signal.SIGALRM, _alarm)


def outcome(function, args, limit=0.25):
    """Run on a deep copy; return a comparable outcome including the post-call argument state."""
    working = copy.deepcopy(args)
    signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        result = ("return", canon(function(*working)))
    except CallTimeout:
        result = ("timeout",)
    except RecursionError:
        result = ("raise", "RecursionError")
    except Exception as error:  # noqa: BLE001 - exception class is the observable
        result = ("raise", type(error).__name__)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    return result, canon(working)


# ---------------------------------------------------------------------------
UNICODE_DIGITS = "٠١٢٣٤٥٦٧٨٩"            # ARABIC-INDIC
FULLWIDTH_DIGITS = "０１２３４５６７８９"
DEVANAGARI_DIGITS = "०१२३४५६७८९"


def fullwidth(char):
    return chr(ord(char) + 0xFEE0) if "!" <= char <= "~" else char


def string_variants(text, rng, alphabet):
    out = {text, text.upper(), text.lower(), text.swapcase(), text + text, text[:-1], text[1:], " " + text, text + " "}
    for i, char in enumerate(text):
        if char.isdigit():
            d = int(char)
            for table in (UNICODE_DIGITS, FULLWIDTH_DIGITS, DEVANAGARI_DIGITS):
                out.add(text[:i] + table[d] + text[i + 1:])
            out.add("".join(UNICODE_DIGITS[int(c)] if c.isdigit() else c for c in text))
        if char.isalpha():
            out.add(text[:i] + fullwidth(char) + text[i + 1:])
            out.add(text[:i] + char.swapcase() + text[i + 1:])
            out.add(text[:i] + {"a": "á", "e": "é", "i": "İ", "o": "ö", "u": "ü"}.get(char.lower(), "é") + text[i + 1:])
        if not char.isalnum():
            out.add(text[:i] + fullwidth(char) + text[i + 1:])
        out.add(text[:i] + text[i + 1:])
        out.add(text[:i] + char + text[i:])
        out.add(text[:i] + rng.choice(alphabet) + text[i + 1:])
    out.add("".join(fullwidth(c) for c in text))
    for repeat in range(1, 40):
        if text:
            digits = [c for c in text if c.isdigit()]
            if digits:
                out.add(text + digits[-1] * repeat)
    return out


def literal_ints(source):
    values = set()
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type == tokenize.NUMBER and tok.string.isdigit():
            values.add(int(tok.string))
        if tok.type == tokenize.STRING:
            values.update(int(x) for x in re.findall(r"\d+", tok.string))
    return values


def int_pool(source, rng):
    pool = set(range(-4, 5))
    for value in literal_ints(source):
        for delta in (-2, -1, 0, 1, 2):
            pool.add(value + delta); pool.add(-(value + delta))
    pool.update([10, 12, 13, 16, 17, 25, 26, 27, 32, 33, 59, 60, 99, 100, 255, 256, 701, 702, 703,
                 999, 1000, 3599, 3600, 3999, 4000, 9999, 10000, 18277, 18278, 18279, 86399, 86400])
    pool.update(rng.randint(-20000, 20000) for _ in range(30))
    return sorted(pool)


WRONG_SCALARS = [1.5, -1.5, "x", "1", None, b"1", [1], (1,), True, False]


def build_probes(schemas, value_args, error_args, body, seed=20261105, random_count=2500):
    """Return a deterministic, de-duplicated list of argument tuples."""
    rng = random.Random(seed)
    ints = int_pool(body, rng)
    small = [v for v in ints if -30 <= v <= 300]
    strings = set()
    for args in value_args + error_args:
        for a in args:
            if type(a) is str:
                strings.add(a)
            if type(a) is list:
                strings.update(x for x in a if type(x) is str)
    alphabet = sorted(set("".join(strings)) | set("aA0 ,#-[]:=/().") ) or list("ab")
    str_pool = set()
    for s in sorted(strings):
        str_pool |= string_variants(s, rng, alphabet)
    for _ in range(300):
        length = rng.randint(0, 40)
        str_pool.add("".join(rng.choice(alphabet) for _ in range(length)))
    for n in range(0, 15):
        str_pool.add("1" + "0" * n); str_pool.add("9" * (n + 1)); str_pool.add("1" * (n + 1) + "," + "2" * (n + 1))
    str_pool |= {"", "A", "a", "É", "é", "ß", "İ", "ǅ", "\t\t", "a\t\tb", "a　b", "a  b", " ", "١", "１", "ａ", "Ａ"}
    str_pool = sorted(str_pool)
    token_pool = sorted({x for args in value_args for a in args if type(a) is list for x in a if type(x) is str} | {"1", "2", "+", "-", "*", "0", "-0", "١", "１", "9999", "10000", "x"})

    def gen(schema, wrong=False):
        if schema == "int":
            return rng.choice(WRONG_SCALARS + [IntChild(rng.choice(small)), "3"]) if wrong else rng.choice(ints if rng.random() < 0.3 else small)
        if schema == "str":
            return rng.choice([StrChild(rng.choice(str_pool)), 1, None, b"ab", ["a"]]) if wrong else rng.choice(str_pool)
        if schema in ("ints", "strs", "matrix", "pairs"):
            n = rng.randint(0, 6)
            item = {"ints": lambda: rng.choice(small), "strs": lambda: rng.choice(token_pool),
                    "matrix": lambda: [rng.choice(small) for _ in range(width)],
                    "pairs": lambda: tuple(sorted(rng.sample(small, 2)))}[schema]
            width = rng.randint(0, 3)
            values = [item() for _ in range(n)]
            if rng.random() < 0.4 and schema in ("ints", "strs"):
                values.sort()
            if wrong:
                kind = rng.randint(0, 2)
                if kind == 0:
                    return rng.choice([tuple(values), ListChild(values), None, "abc", 3])
                bad = {"ints": WRONG_SCALARS + [IntChild(1)], "strs": [1, None, StrChild("1"), b"1", ["1"]],
                       "matrix": [(1, 2), ListChild([1]), None, "ab", [1.5], ["x"], [True], [IntChild(1)]],
                       "pairs": [[1, 2], TupleChild((1, 2)), None, (1, 2, 3), (1,), (True, 2), (IntChild(1), 2), ("x", 2), (1.5, 2)]}[schema]
                values.insert(rng.randint(0, len(values)), rng.choice(bad))
            return values
        if schema in ("tuple3", "pair"):
            n = 3 if schema == "tuple3" else 2
            values = tuple(rng.choice(small[:20] + [0, 1, 2, 3]) for _ in range(n))
            if wrong:
                return rng.choice([list(values), TupleChild(values), values[:-1], values + (1,), (True,) + values[1:], ("x",) + values[1:], (IntChild(1),) + values[1:], (1.5,) + values[1:], None])
            return values
        if schema == "objects":
            values = tuple(rng.choice([1, "a", [1], (2,), None, 3.5, [], "b"]) for _ in range(rng.randint(0, 5)))
            return rng.choice([list(values), TupleChild(values), None, "abc"]) if wrong else values
        raise AssertionError(schema)

    probes = []
    seen = set()

    def push(args):
        key = args_repr(args)
        if key not in seen:
            seen.add(key)
            probes.append(tuple(args))

    for args in value_args + error_args:
        push(args)
    # single-position substitutions around every gold valid case
    for base in value_args:
        for pos, schema in enumerate(schemas):
            pool = []
            if schema == "int":
                pool = ints + WRONG_SCALARS + [IntChild(v) for v in (0, 1, 2)]
            elif schema == "str":
                pool = str_pool + [StrChild(s) for s in str_pool[:5]] + [1, None, b"a"]
            else:
                pool = [gen(schema) for _ in range(60)] + [gen(schema, wrong=True) for _ in range(60)]
            for value in pool:
                args = list(base); args[pos] = value; push(args)
        # element-level substitutions for list arguments of the gold cases
        for pos, schema in enumerate(schemas):
            if schema in ("ints", "strs", "matrix", "pairs") and type(base[pos]) is list:
                bad = {"ints": WRONG_SCALARS + [IntChild(1), 256, -1, 300, 10 ** 13],
                       "strs": [1, None, StrChild("1"), b"1", "١", "１", "x", "10000"],
                       "matrix": [(1,), ListChild([1]), None, [1.5], ["x"], [True], [IntChild(1)], [1, 2, 3, 4]],
                       "pairs": [[1, 2], TupleChild((1, 2)), None, (1, 2, 3), (2, 1), (True, 2), (IntChild(1), 2), ("x", 2), (1.5, 2), (1, IntChild(5))]}[schema]
                for value in bad:
                    for where in range(len(base[pos]) + 1):
                        items = list(base[pos]); items.insert(where, value)
                        args = list(base); args[pos] = items; push(args)
                    if base[pos]:
                        items = list(base[pos]); items[0] = value
                        args = list(base); args[pos] = items; push(args)
                        items = [value] * len(base[pos])
                        args = list(base); args[pos] = items; push(args)
                    args = list(base); args[pos] = [value]; push(args)
                    args = list(base); args[pos] = [value, value]; push(args)
    # mixed-invalid pairs: one type-invalid position plus one value-invalid position
    for base in value_args:
        for p1, s1 in enumerate(schemas):
            for p2, s2 in enumerate(schemas):
                if p1 == p2:
                    continue
                for _ in range(25):
                    args = list(base); args[p1] = gen(s1, wrong=True); args[p2] = gen(s2); push(args)
        for pos, schema in enumerate(schemas):
            if schema in ("ints", "pairs", "matrix", "strs"):
                for _ in range(40):
                    args = list(base); value = gen(schema, wrong=True)
                    if type(value) is list:
                        value.append(rng.choice([-1, 256, 300, 10 ** 13, (5, 1), "x", "١"]) if schema != "matrix" else [1, 2, 3, 4, 5])
                        args[pos] = value; push(args)
    # random tuples
    for _ in range(random_count):
        args = [gen(s, wrong=rng.random() < 0.15) for s in schemas]
        push(args)
    return probes
