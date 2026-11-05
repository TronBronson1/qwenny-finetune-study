"""Prove rubric gaps behaviourally: build a mutant that violates a rubric item,
run the GOLD suite against reference and mutant. If the gold suite passes the
mutant, the gold target does not test that rubric item.

Reads candidate-006 (read-only); all copies and pytest runs live under argv[2].
"""
import os, re, sys, shutil, subprocess, json

ROOT = sys.argv[1]
WORK = os.path.join(sys.argv[2], "rubric_mutants")
PY = sys.executable

NORM = "''.join(str(int(c)) if c.isdigit() else c for c in text)"

MUTANTS = {
    # rubric item violated -> (task path, old, new)
    "TR038 accepts non-ASCII digits": ("training/TR038", 'r"[0-9a-fA-F]{2}",text', 'r"[0-9a-fA-F]{2}",' + NORM),
    "TR043 accepts non-ASCII digits": ("training/TR043", 'r"[01]{1,32}",text', 'r"[01]{1,32}",' + NORM),
    "TR044 accepts non-ASCII digits": ("training/TR044", '+r"\\]",text)', '+r"\\]",' + NORM + ')'),
    "TR056 accepts non-ASCII digits": ("training/TR056", 'r"#[0-9a-fA-F]{6}",text', 'r"#[0-9a-fA-F]{6}",' + NORM),
    "DV010 accepts non-ASCII digits": ("development/DV010", 'r"-?(?:0|[1-9][0-9]{0,3})",token', 'r"-?(?:0|[1-9][0-9]{0,3})",' + NORM.replace("text", "token")),
    "DV008 compares case-insensitively": ("development/DV008", "(a!=b)", "(a.lower()!=b.lower())"),
    "DV011 accepts int-subclass endpoints": ("development/DV011", "_types((intervals,), ('pairs',))",
        "_exact(intervals, list)\n"
        "    for p in intervals:\n"
        "        _exact(p, tuple)\n"
        "        for x in p:\n"
        "            if not isinstance(x, int) or type(x) is bool: raise TypeError('int')\n"
        "    if any(len(p) != 2 for p in intervals): raise ValueError('pair shape')"),
    # Control: an ordinary-element-type gap (rubric pedantry check)
    "TR027 element check only rejects bool/subclass": ("training/TR027", "_types((values,), ('ints',))",
        "_exact(values, list)\n"
        "    for x in values:\n"
        "        if isinstance(x, int) and type(x) is not int: raise TypeError('int')"),
}


def run(dirpath):
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_target.py"], cwd=dirpath, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    last = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()][-1]
    return r.returncode, last


results = {}
for label, (task, old, new) in MUTANTS.items():
    src = os.path.join(ROOT, "tasks", task)
    target = open(os.path.join(src, "TARGET.md"), encoding="utf-8").read()
    test_code = re.search(r"```python\n(.*?)```", target, re.S).group(1)
    ref = open(os.path.join(src, "evaluator", "reference", "subject.py"), encoding="utf-8").read()
    assert ref.count(old) == 1, (label, "patch anchor not found exactly once")
    out = {}
    for variant, code in (("reference", ref), ("rubric_mutant", ref.replace(old, new))):
        d = os.path.join(WORK, task.replace("/", "_"), variant)
        assert not os.path.exists(d), "Refuse to overwrite a previous replay"
        os.makedirs(d)
        open(os.path.join(d, "subject.py"), "w", encoding="utf-8").write(code)
        open(os.path.join(d, "test_target.py"), "w", encoding="utf-8").write(test_code)
        out[variant] = run(d)
    gap = out["reference"][0] == 0 and out["rubric_mutant"][0] == 0
    results[label] = dict(out, gold_misses_rubric_item=gap)
    print(f"{label:48s} ref={out['reference'][1]:28s} mutant={out['rubric_mutant'][1]:28s} -> {'GOLD MISSES IT' if gap else 'gold catches it'}")

json.dump(results, open(os.path.join(sys.argv[2], "rubric_mutants.json"), "w"), indent=1)
