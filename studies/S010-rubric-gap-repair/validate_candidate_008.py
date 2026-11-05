"""Calibration gate for candidate-008 (S010).

    python3 studies/S010-rubric-gap-repair/validate_candidate_008.py

For every task: the gold suite must pass the unchanged reference with >=1 test and no skips;
every designated mutant must fail with its declared witness node among the failures.
Isolated temp dirs, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, -p no:cacheprovider, per-run timeout.
Writes validation-001/summary.json. Candidate files are verified against SHA256.json first.
"""
import argparse
import concurrent.futures as futures
import hashlib, json, os, pathlib, platform, shutil, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
EXP = HERE.parents[1]
C8 = EXP / "dataset-v1" / "candidate-008"
OUT = HERE / "validation-001"  # default; override with --out
TIMEOUT = 120


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(test_file, subject_file):
    with tempfile.TemporaryDirectory(prefix="s010-", ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        shutil.copy(test_file, tmp / "test_target.py"); shutil.copy(subject_file, tmp / "subject.py")
        (tmp / "pytest.ini").write_text("[pytest]\n")
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST")}
        env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-c", str(tmp / "pytest.ini"), "--rootdir", str(tmp),
               "--junitxml", str(tmp / "junit.xml"), "test_target.py"]
        start = time.monotonic()
        try:
            proc = subprocess.run(cmd, cwd=tmp, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return dict(exit_code=None, timeout=True, seconds=round(time.monotonic() - start, 2))
        out = dict(exit_code=proc.returncode, timeout=False, seconds=round(time.monotonic() - start, 2))
        suite = ET.parse(tmp / "junit.xml").getroot()
        suite = suite if suite.tag == "testsuite" else suite.find("testsuite")
        out.update(tests=int(suite.get("tests")), failures=int(suite.get("failures")), errors=int(suite.get("errors")), skipped=int(suite.get("skipped")))
        out["failed_nodes"] = [f"test_target.py::{c.get('name')}" for c in suite.iter("testcase") if c.find("failure") is not None or c.find("error") is not None]
        return out


def main():
    global OUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="output directory (default: validation-001 next to this script)")
    parser.add_argument("--note", default="Linux validation; established Python 3.15 / pytest 9.2 Windows validation remains required before training use.")
    cli = parser.parse_args()
    if cli.out:
        OUT = pathlib.Path(cli.out)
    digests = json.loads((C8 / "SHA256.json").read_text(encoding="utf-8"))
    bad = [name for name, digest in digests.items() if sha(C8 / name) != digest]
    assert not bad, f"candidate-008 files changed since build: {bad[:5]}"
    jobs = []
    for split in ("training", "development"):
        for task in sorted((C8 / "tasks" / split).iterdir()):
            jobs.append((task.name, "reference", task / "test_target.py", task / "evaluator/reference/subject.py", None))
            for m in json.loads((task / "evaluator/mutants.json").read_text(encoding="utf-8")):
                jobs.append((task.name, m["id"], task / "test_target.py", task / "evaluator/mutants" / m["id"] / "subject.py", m["witness"]["node"]))
    results, failures = [], []
    with futures.ThreadPoolExecutor(os.cpu_count() or 2) as pool:
        mapping = {pool.submit(run, j[2], j[3]): j for j in jobs}
        for f in futures.as_completed(mapping):
            task, variant, _, _, node = mapping[f]
            r = f.result()
            if variant == "reference":
                ok = r.get("exit_code") == 0 and r.get("tests", 0) > 0 and r.get("skipped", 1) == 0
                why = None if ok else "reference not accepted"
            else:
                ok = r.get("exit_code") == 1 and node in r.get("failed_nodes", [])
                why = None if ok else ("declared witness node did not fail" if r.get("exit_code") == 1 else "mutant not rejected")
            row = dict(task=task, variant=variant, witness_node=node, passed_gate=ok, **{k: v for k, v in r.items() if k != "failed_nodes"},
                       witness_failed=None if node is None else node in r.get("failed_nodes", []))
            results.append(row)
            if not ok:
                failures.append(dict(task=task, variant=variant, reason=why, exit_code=r.get("exit_code")))
    results.sort(key=lambda x: (x["task"], x["variant"] != "reference", x["variant"]))
    refs = [r for r in results if r["variant"] == "reference"]
    import pytest
    summary = dict(status="passed" if not failures else "failed", candidate="candidate-008", candidate_manifest_sha256=sha(C8 / "SHA256.json"),
                   runtime=f"{platform.python_version()} / pytest {pytest.__version__} / {platform.platform()}",
                   reference_suites=len(refs), reference_cases=sum(r.get("tests", 0) for r in refs),
                   designated_mutants=len(results) - len(refs), failures=failures, results=results,
                   note=cli.note)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("status", "reference_suites", "reference_cases", "designated_mutants")} | {"failures": failures[:10]}, indent=2))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
