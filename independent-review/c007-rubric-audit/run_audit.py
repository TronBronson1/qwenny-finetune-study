#!/usr/bin/env python3
"""Independent rubric-mutant audit of dataset-v1 candidate-006 and candidate-007 gold suites.

One command (from the repository root, with pytest installed):

    python3 independent-review/c007-rubric-audit/run_audit.py

Stages
  1. build   - generate single-requirement rubric mutants for every training/development task
  2. witness - search deterministic probes for a concrete input on which each mutant differs
  3. verify  - re-check every witness in a fresh subprocess from the written mutant files
  4. gold    - run each candidate's gold suite (test_target.py) against the reference and each
               confirmed mutant with pytest (plugin autoload off, per-run timeout)
  5. report  - write results/*.json and REPORT.md

Repository files are only read. Generated mutant sources go to build/ (git-ignored).
"""
import argparse
import ast
import concurrent.futures as futures
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import mutants_lib  # noqa: E402
import probes as P  # noqa: E402

CANDIDATES = ("candidate-006", "candidate-007")
SPLITS = ("training", "development")
BUILD = HERE / "build"
RESULTS = HERE / "results"
PYTEST_TIMEOUT = 120


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def task_dirs(candidate):
    root = REPO / "dataset-v1" / candidate / "tasks"
    out = {}
    for split in SPLITS:
        for path in sorted((root / split).iterdir()):
            if path.is_dir():
                out[path.name] = (split, path)
    return out


def load_cases(path):
    cases = json.loads((path / "evaluator" / "cases.json").read_text())
    value, error = [], []
    for case in cases:
        args = eval(case["args_python"], dict(P.NAMESPACE))  # noqa: S307 - repository fixtures
        (value if "expected_python" in case else error).append(args)
    return value, error


def exec_module(source, label):
    namespace = {"__name__": label}
    exec(compile(source, label, "exec"), namespace)  # noqa: S102 - generated local mutant
    return namespace


# ---------------------------------------------------------------------------
def stage_witness(task_ids, tasks7, tasks6):
    records = {}
    for tid in task_ids:
        split, path7 = tasks7[tid]
        path6 = tasks6[tid][1]
        ref_bytes = (path7 / "evaluator" / "reference" / "subject.py").read_bytes()
        ref6_bytes = (path6 / "evaluator" / "reference" / "subject.py").read_bytes()
        source = ref_bytes.decode()
        spec = (path7 / "SPEC.md").read_text()
        info = mutants_lib.parse_reference(source)
        value7, error7 = load_cases(path7)
        value6, error6 = load_cases(path6)
        reference = exec_module(source, f"{tid}-reference")[info["name"]]
        body = source[info["body_start"]:]
        probes = P.build_probes(info["schemas"], value7 + value6, error7 + error6, body)
        ref_out = [P.outcome(reference, args) for args in probes]
        raised = {o[0][1] for o in ref_out if o[0][0] == "raise"}
        depth = max((canon_depth(o[0][1]) for o in ref_out if o[0][0] == "return"), default=0)
        base_args = [P.pyrepr(a) for a in value7[0]]
        info, mutants = mutants_lib.build_mutants(tid, source, spec, base_args, raised, depth)
        entries = []
        for mutant in mutants:
            try:
                function = exec_module(mutant["source"], f"{tid}-{mutant['id']}")[info["name"]]
            except Exception as error:  # noqa: BLE001
                entries.append({**strip(mutant), "status": "build-error", "error": repr(error)})
                continue
            witness, budget = None, None
            for args, expected in zip(probes, ref_out):
                if budget is not None:
                    budget -= 1
                    if budget < 0:
                        break
                got = P.outcome(function, args)
                if got != expected:
                    text = P.args_repr(args)
                    if witness is None or len(text) < len(witness["args_python"]):
                        witness = {"args_python": text, "reference": describe(expected), "mutant": describe(got)}
                    if budget is None:
                        budget = 400  # keep scanning briefly for a shorter witness
            entries.append({**strip(mutant), "status": "differs" if witness else "no-difference-found",
                            "witness": witness, "source_sha256": sha256(mutant["source"])})
            out_dir = BUILD / "mutants" / tid / mutant["id"]
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "subject.py").write_text(mutant["source"])
        records[tid] = {
            "task": tid, "split": split, "function": info["name"], "params": list(info["params"]),
            "schemas": list(info["schemas"]), "spec_flags": mutants_lib.spec_flags(spec),
            "reference_sha256": sha256(ref_bytes), "reference_identical_006_007": ref_bytes == ref6_bytes,
            "probe_count": len(probes), "reference_raises": sorted(raised), "return_depth": depth,
            "mutants": entries,
        }
        n_diff = sum(e["status"] == "differs" for e in entries)
        print(f"[witness] {tid}: {len(entries)} mutants, {n_diff} differ, {len(probes)} probes", flush=True)
    return records


def canon_depth(c):
    """Container nesting depth of a canonical value (0 for scalars)."""
    if not (isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], str)):
        return 0
    payload = c[1]
    if isinstance(payload, tuple) and c[0] not in ("str", "int", "bool", "float", "NoneType"):
        return 1 + max((canon_depth(x) for x in payload), default=0)
    return 0


def describe(out):
    result, post = out
    return {"outcome": result[0], "value": repr(result[1]) if len(result) > 1 else None, "post_args": repr(post)}


def strip(mutant):
    return {k: v for k, v in mutant.items() if k != "source"}


# ---------------------------------------------------------------------------
VERIFY_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import probes as P
spec = json.loads(sys.stdin.read())
out = {}
def load(path, name):
    ns = {"__name__": "verify"}
    exec(compile(open(path).read(), path, "exec"), ns)
    return ns[name]
reference = load(spec["reference"], spec["function"])
for mid, (path, witness) in spec["mutants"].items():
    args = eval(witness, dict(P.NAMESPACE))
    a = P.outcome(reference, args)
    b = P.outcome(load(path, spec["function"]), eval(witness, dict(P.NAMESPACE)))
    out[mid] = {"confirmed": a != b, "reference": repr(a), "mutant": repr(b)}
print(json.dumps(out))
'''


def stage_verify(records, tasks7):
    for tid, record in records.items():
        payload = {"reference": str(tasks7[tid][1] / "evaluator" / "reference" / "subject.py"),
                   "function": record["function"], "mutants": {}}
        for m in record["mutants"]:
            if m["status"] == "differs":
                payload["mutants"][m["id"]] = (str(BUILD / "mutants" / tid / m["id"] / "subject.py"), m["witness"]["args_python"])
        proc = subprocess.run([sys.executable, "-I", "-c", VERIFY_CODE, str(HERE)], input=json.dumps(payload),
                              capture_output=True, text=True, timeout=600)
        if proc.returncode:
            raise RuntimeError(f"verify failed for {tid}: {proc.stderr}")
        checked = json.loads(proc.stdout)
        for m in record["mutants"]:
            if m["id"] in checked:
                m["witness_confirmed_fresh_process"] = checked[m["id"]]["confirmed"]
                if not checked[m["id"]]["confirmed"]:
                    m["status"] = "witness-not-reproduced"
        print(f"[verify] {tid}: {sum(v['confirmed'] for v in checked.values())}/{len(checked)} confirmed", flush=True)


# ---------------------------------------------------------------------------
def run_gold(test_file, subject_file):
    with tempfile.TemporaryDirectory(prefix="gold-") as tmp:
        tmp = Path(tmp)
        shutil.copy(test_file, tmp / "test_target.py")
        shutil.copy(subject_file, tmp / "subject.py")
        (tmp / "pytest.ini").write_text("[pytest]\n")
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST")}
        env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-c", str(tmp / "pytest.ini"),
               "--rootdir", str(tmp), "--junitxml", str(tmp / "junit.xml"), "test_target.py"]
        start = time.monotonic()
        try:
            proc = subprocess.run(cmd, cwd=tmp, env=env, capture_output=True, text=True, timeout=PYTEST_TIMEOUT)
        except subprocess.TimeoutExpired:
            return {"exit_code": None, "timeout": True, "seconds": round(time.monotonic() - start, 2)}
        result = {"exit_code": proc.returncode, "timeout": False, "seconds": round(time.monotonic() - start, 2)}
        try:
            root = ET.parse(tmp / "junit.xml").getroot()
            suite = root if root.tag == "testsuite" else root.find("testsuite")
            result.update(tests=int(suite.get("tests")), failures=int(suite.get("failures")),
                          errors=int(suite.get("errors")), skipped=int(suite.get("skipped")))
            result["failed_tests"] = [case.get("name") for case in suite.iter("testcase")
                                      if case.find("failure") is not None or case.find("error") is not None][:10]
        except (OSError, ET.ParseError) as error:
            result["junit_error"] = repr(error)
            result["stdout_tail"] = proc.stdout[-800:]
        return result


def classify(run):
    if run.get("timeout"):
        return "timeout"
    if run["exit_code"] == 0 and run.get("tests", 0) > 0:
        return "passed"
    if run["exit_code"] == 1:
        return "failed"
    return f"error-exit-{run['exit_code']}"


def stage_gold(records, task_map, workers):
    jobs = []
    for candidate in CANDIDATES:
        tasks = task_map[candidate]
        for tid, record in records.items():
            test_file = tasks[tid][1] / "test_target.py"
            jobs.append((candidate, tid, "__reference__", test_file, tasks[tid][1] / "evaluator" / "reference" / "subject.py"))
            for m in record["mutants"]:
                if m["status"] == "differs":
                    jobs.append((candidate, tid, m["id"], test_file, BUILD / "mutants" / tid / m["id"] / "subject.py"))
    print(f"[gold] {len(jobs)} pytest runs with {workers} workers", flush=True)
    results = {}
    with futures.ThreadPoolExecutor(workers) as pool:
        future_map = {pool.submit(run_gold, j[3], j[4]): j for j in jobs}
        for done, future in enumerate(futures.as_completed(future_map), 1):
            candidate, tid, mid, *_ = future_map[future]
            run = future.result()
            run["verdict"] = classify(run)
            results[(candidate, tid, mid)] = run
            if done % 250 == 0:
                print(f"[gold] {done}/{len(jobs)}", flush=True)
    for tid, record in records.items():
        record["gold"] = {}
        for candidate in CANDIDATES:
            ref = results[(candidate, tid, "__reference__")]
            record["gold"][candidate] = {
                "test_sha256": sha256((task_map[candidate][tid][1] / "test_target.py").read_bytes()),
                "reference": ref,
            }
        for m in record["mutants"]:
            m["gold"] = {c: results[(c, tid, m["id"])] for c in CANDIDATES if (c, tid, m["id"]) in results}


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tasks", nargs="*", help="limit to these task ids (default: all)")
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 2)
    parser.add_argument("--skip-gold", action="store_true")
    args = parser.parse_args()

    try:
        import pytest  # noqa: F401
    except ImportError:
        sys.exit("pytest is required: python3 -m pip install pytest")
    started = time.time()
    if BUILD.exists():
        shutil.rmtree(BUILD / "mutants", ignore_errors=True)
    BUILD.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    task_map = {c: task_dirs(c) for c in CANDIDATES}
    ids = sorted(set(task_map["candidate-007"]) & set(task_map["candidate-006"]))
    if args.tasks:
        ids = [t for t in ids if t in args.tasks]
    assert not any(t.startswith(("EV", "RG")) for t in ids), "final/regression tasks must not be audited"
    records = stage_witness(ids, task_map["candidate-007"], task_map["candidate-006"])
    stage_verify(records, task_map["candidate-007"])
    if not args.skip_gold:
        stage_gold(records, task_map, args.workers)
    import pytest as _pytest
    meta = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_seconds": round(time.time() - started, 1),
        "python": sys.version.split()[0], "pytest": _pytest.__version__, "platform": platform.platform(),
        "repo_commit": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
        "candidates": list(CANDIDATES), "tasks": len(ids),
        "pytest_flags": "PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, -p no:cacheprovider, isolated temp dir, timeout %ss" % PYTEST_TIMEOUT,
        "script_sha256": {p.name: sha256(p.read_bytes()) for p in sorted(HERE.glob("*.py"))},
    }
    full = {"meta": meta, "tasks": records}
    (RESULTS / "audit-results.json").write_text(json.dumps(full, indent=1, sort_keys=True))
    subprocess.run([sys.executable, str(HERE / "make_report.py")], check=True)
    print(f"done in {meta['elapsed_seconds']} s")


if __name__ == "__main__":
    main()
