"""Read-only check: do gold TARGET.md suites satisfy the generic S006 rubric rules?

Reads candidate-006 training/development tasks only. Never imports or executes
task code; writes output only to the directory given as argv[2].
"""
import ast, json, os, re, sys, glob, collections

ROOT = sys.argv[1]
OUT = sys.argv[2]
SPLITS = ("training", "development")

SCALAR = {"int": int, "str": str, "bytes": bytes}


def code_block(text):
    m = re.search(r"```python\n(.*?)```", text, re.S)
    return m.group(1)


def build(node, classes):
    """Turn a literal AST into a real object; *Child(...) -> real subclass instance."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -build(node.operand, classes)
    if isinstance(node, ast.Tuple):
        return tuple(build(e, classes) for e in node.elts)
    if isinstance(node, ast.List):
        return [build(e, classes) for e in node.elts]
    if isinstance(node, ast.Dict):
        return {build(k, classes): build(v, classes) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id
        inner = build(node.args[0], classes) if node.args else None
        if name in classes:
            return classes[name](inner) if node.args else classes[name]()
        if name == "iter":
            return iter(inner)
        raise ValueError("unsupported call " + name)
    if isinstance(node, ast.GeneratorExp):
        return (x for x in ())
    raise ValueError("unsupported node " + ast.dump(node)[:80])


def kind_of(v, base):
    if type(v) is base:
        return None
    if isinstance(v, base):
        return "bool" if type(v) is bool else "subclass"
    return "ordinary"


def violations(v, schema, level="arg"):
    """Return list of (level, kind) type violations of v against schema."""
    out = []
    if schema in SCALAR:
        k = kind_of(v, SCALAR[schema])
        return [(level, k)] if k else []
    if schema == "maybe_strs":
        return [] if v is None else violations(v, "strs", level)
    if schema == "stream":
        return [] if type(v).__name__ in ("list", "tuple", "generator", "list_iterator") else [(level, "ordinary")]
    if schema in ("ints", "strs", "matrix", "pairs", "commands"):
        k = kind_of(v, list)
        if k:
            out.append((level, k))
        if isinstance(v, (list, tuple)):
            sub = {"ints": "int", "strs": "str", "matrix": "ints", "pairs": "pair", "commands": None}[schema]
            for item in v:
                if sub is None:
                    kk = kind_of(item, tuple)
                    if kk:
                        out.append((level + ".item", kk))
                else:
                    out += violations(item, sub, level + ".item")
        return out
    if schema in ("pair", "tuple3", "objects"):
        k = kind_of(v, tuple)
        if k:
            out.append((level, k))
        if schema != "objects" and isinstance(v, (list, tuple)):
            for item in v:
                out += violations(item, "int", level + ".item")
        return out
    if schema in ("counts", "aliases"):
        k = kind_of(v, dict)
        if k:
            out.append((level, k))
        if isinstance(v, dict):
            for key, item in v.items():
                out += violations(key, "str", level + ".key")
                out += violations(item, "int" if schema == "counts" else "str", level + ".value")
        return out
    raise ValueError(schema)


def required_kinds(schema):
    """(level -> required kinds) per the rubric note: ordinary + bool/subclass where applicable."""
    def scalar(s):
        return {"ordinary", "subclass", "bool"} if s == "int" else {"ordinary", "subclass"}
    if schema in SCALAR:
        return {"arg": scalar(schema)}
    if schema in ("ints", "strs"):
        return {"arg": {"ordinary", "subclass"}, "arg.item": scalar(schema[:-1])}
    if schema == "matrix":
        return {"arg": {"ordinary", "subclass"}, "arg.item": {"ordinary", "subclass"}, "arg.item.item": scalar("int")}
    if schema == "pairs":
        return {"arg": {"ordinary", "subclass"}, "arg.item": {"ordinary", "subclass"}, "arg.item.item": scalar("int")}
    if schema in ("pair", "tuple3"):
        return {"arg": {"ordinary", "subclass"}, "arg.item": scalar("int")}
    if schema == "commands":
        return {"arg": {"ordinary", "subclass"}, "arg.item": {"ordinary", "subclass"}}
    if schema in ("counts", "aliases"):
        return {"arg": {"ordinary", "subclass"}, "arg.key": scalar("str"),
                "arg.value": scalar("int" if schema == "counts" else "str")}
    if schema == "maybe_strs":
        return {"arg": {"ordinary", "subclass"}, "arg.item": scalar("str")}
    return {"arg": {"ordinary"}}


def strings_in(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from strings_in(k)
            yield from strings_in(v)
    elif isinstance(obj, (list, tuple)):
        for x in obj:
            yield from strings_in(x)


def is_empty_arg(obj):
    return any((isinstance(a, (str, list, tuple, dict, bytes)) and len(a) == 0) for a in obj)


def analyse(task_dir):
    rec = json.load(open(os.path.join(task_dir, "record.json"), encoding="utf-8"))
    spec = open(os.path.join(task_dir, "SPEC.md"), encoding="utf-8").read()
    target = open(os.path.join(task_dir, "TARGET.md"), encoding="utf-8").read()
    tree = ast.parse(code_block(target))
    classes = {}
    for n in tree.body:
        if isinstance(n, ast.ClassDef):
            base = {"int": int, "str": str, "list": list, "tuple": tuple, "dict": dict, "bytes": bytes}[n.bases[0].id]
            classes[n.name] = type(n.name, (base,), {})
    cases = []  # (test_name, args, expected)
    test_bodies = {}
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
        test_bodies[fn.name] = ast.unparse(fn)
        for dec in fn.decorator_list:
            if isinstance(dec, ast.Call) and getattr(dec.func, "attr", "") == "parametrize":
                for p in dec.args[1].elts:
                    args = build(p.args[0], classes)
                    exp = build(p.args[1], classes) if len(p.args) > 1 else None
                    cases.append((fn.name, args, exp))
    schemas = rec["schemas"]
    params = rec["parameters"]
    findings = []

    # 1. Per-position isolated type-rejection coverage
    have = collections.defaultdict(set)
    unexplained_type_cases = 0
    for name, args, _ in cases:
        if name != "test_raises_typeerror":
            continue
        per_pos = [violations(a, s) for a, s in zip(args, schemas)]
        bad = [i for i, v in enumerate(per_pos) if v]
        if not bad:
            unexplained_type_cases += 1
        if len(bad) == 1:
            for level, kind in per_pos[bad[0]]:
                have[(bad[0], level)].add(kind)
    for i, s in enumerate(schemas):
        for level, kinds in required_kinds(s).items():
            missing = kinds - have[(i, level)]
            if missing:
                findings.append(f"type-rejection gap: {params[i]} [{level}] missing {sorted(missing)}")
    if unexplained_type_cases:
        findings.append(f"{unexplained_type_cases} TypeError case(s) with no detectable type violation (review)")

    # 2. Exact output type and mutation check in value test
    vb = test_bodies.get("test_values", "")
    if "assert_exact_shape(actual" not in vb:
        findings.append("value test lacks exact-type assertion")
    mutable = any(s not in ("int", "str", "bytes") for s in schemas)
    if mutable and "deepcopy" not in vb:
        findings.append("mutable input but no before/after mutation comparison")

    # 3. Type-before-value witness where both classes exist
    body = spec.split("Write one complete pytest file")[0]
    has_value_exc = ("ValueError" in body) or ("IndexError" in body)
    if has_value_exc and rec.get("type_before_value_witnesses", 0) == 0:
        findings.append("spec has ValueError/IndexError but record lists 0 type-before-value witnesses")
    if "ValueError" in body and "IndexError" in body:
        findings.append("MANUAL: spec has shape(ValueError)-before-bounds(IndexError); confirm a mixed witness")

    # 4. Spec keyword triggers
    value_strs = [s for name, args, _ in cases if name == "test_values" for s in strings_in(args)]
    all_strs = [s for _, args, _ in cases for s in strings_in(args)]
    low = body.lower()
    if "case-sensitive" in low or "case-sensitively" in low:
        ok = False
        for name, args, _ in cases:
            if name != "test_values":
                continue
            ss = [a for a in args if isinstance(a, str)]
            if len(ss) >= 2 and any(x != y and x.lower() == y.lower() for x in ss for y in ss):
                ok = True
            if any(re.search(r"[A-Z]", x) and re.search(r"[a-z]", x) for x in ss) and len(ss) >= 2:
                ok = ok or any(x.lower() != x and y.lower() == x.lower() for x in ss for y in ss if x != y)
        if not ok:
            findings.append("spec says case-sensitive but no value case with strings differing only by case")
    if "case-insensitive" in low and not any(re.search(r"[A-Z]", s) and re.search(r"[a-z]", s) for s in value_strs):
        findings.append("spec says case-insensitive but no mixed-case value input")
    if "ascii" in low and not any(any(ord(c) > 127 for c in s) for s in all_strs):
        findings.append("spec restricts to ASCII but no case uses a non-ASCII character")
    if "unicode" in low and not any(any(ord(c) > 127 for c in s) for s in value_strs):
        findings.append("spec mentions Unicode but no value case uses a non-ASCII character")
    if "empty" in low and not any(is_empty_arg(args) for name, args, _ in cases if name == "test_values"):
        findings.append("spec mentions empty input but no empty value case")

    n_val = sum(1 for c in cases if c[0] == "test_values")
    return dict(id=rec["id"], split=rec["split"], family=rec["family"], schemas=schemas,
                value_cases=n_val, exception_cases=len(cases) - n_val, findings=findings)


def main():
    results = []
    for split in SPLITS:
        for d in sorted(glob.glob(os.path.join(ROOT, "tasks", split, "*"))):
            try:
                results.append(analyse(d))
            except Exception as e:  # report, do not hide
                results.append(dict(id=os.path.basename(d), split=split, error=repr(e), findings=["ANALYSIS ERROR"]))
    json.dump(results, open(os.path.join(OUT, "gold_rubric_check.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    auto = [r for r in results if any(not f.startswith("MANUAL") for f in r["findings"])]
    print(f"tasks checked: {len(results)}; with at least one automatic finding: {len(auto)}")
    cat = collections.Counter()
    for r in results:
        for f in r["findings"]:
            cat[re.sub(r":.*", "", f) if f.startswith("type-rejection") else f.split(" (")[0][:70]] += 1
    for k, v in cat.most_common():
        print(f"{v:3d}  {k}")
    print()
    for r in results:
        if r["findings"]:
            print(r["id"], r.get("family"), r.get("schemas"), f"val={r.get('value_cases')} exc={r.get('exception_cases')}")
            for f in r["findings"]:
                print("    -", f)


main()
