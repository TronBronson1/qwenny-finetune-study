#!/usr/bin/env python3
"""Reference implementation of the proposed pre-registered adoption decision (PREREGISTRATION_PROPOSAL.md).

    python independent-review/power-sim/decide.py outcomes.csv [--out decision.json]
    python independent-review/power-sim/decide.py --self-test

Input CSV columns (one row per split/task/arm/seed, first-attempt outcomes only, no best-of selection):
    split            heldout | regression
    task             task id
    arm              B | C
    seed             17 | 42 | 73
    accepted         1 if strictly accepted (held-out) / passed (regression), else 0
    fabricated_claim optional; 1 if the answer contains an unsupported execution claim

Only numpy is required. The exact one-sided sign-flip p-value enumerates all 2^n sign patterns
(meet-in-the-middle), so it is deterministic. The 95 % interval is descriptive (test inversion
with a fixed-seed Monte-Carlo sign-flip) and is not part of the decision.
"""
import argparse, csv, json, sys
from collections import defaultdict
import numpy as np

SEEDS = (17, 42, 73)
THRESHOLD = 0.10
ALPHA_ONE_SIDED = 0.025
REGRESSION_TOLERANCE = 2          # guard fails at >= 3 more majority-failed regression tasks for C
EXPECTED = {"heldout": 24, "regression": 12}


def exact_signflip_p(d):
    """P(mean of randomly sign-flipped |d| >= observed mean), exact over all 2^n patterns."""
    d = np.asarray(d, dtype=float)
    observed = d.sum()
    a = np.abs(d)
    half = len(a) // 2

    def sums(values):
        out = np.zeros(1)
        for v in values:
            out = np.concatenate([out + v, out - v])
        return out
    left, right = np.sort(sums(a[:half])), sums(a[half:])
    tol = 1e-9 * max(1.0, a.sum())
    # count pairs with left + right >= observed - tol
    counts = len(left) - np.searchsorted(left, observed - tol - right, side="left")
    return float(counts.sum()) / float(len(left) * len(right))


def mc_interval(d, level=0.95, flips=20000, seed=20261105):
    """Descriptive test-inversion interval for the mean shift (Monte-Carlo sign-flip, fixed seed)."""
    d = np.asarray(d, dtype=float)
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1.0, 1.0], size=(flips, len(d)))
    grid = np.linspace(-1, 1, 801)
    keep = []
    for shift in grid:
        x = d - shift
        null = np.abs((signs * x).mean(1))
        p = (1 + (null >= abs(x.mean()) - 1e-12).sum()) / (flips + 1)
        if p > 1 - level:
            keep.append(shift)
    return (float(min(keep)), float(max(keep))) if keep else (None, None)


def load(path):
    table = defaultdict(dict)
    fabricated = defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["split"].strip(), row["task"].strip(), row["arm"].strip(), int(row["seed"]))
            assert key[0] in EXPECTED and key[2] in ("B", "C") and key[3] in SEEDS, f"bad row {row}"
            assert key not in table, f"duplicate row {key} (one sample per task/arm/seed)"
            table[key] = int(row["accepted"])
            if row.get("fabricated_claim", "").strip() in ("1", "true", "True"):
                fabricated[key[2]] += 1
    return table, fabricated


def decide(table, fabricated):
    problems = []
    tasks = {s: sorted({k[1] for k in table if k[0] == s}) for s in EXPECTED}
    for split, n in EXPECTED.items():
        if len(tasks[split]) != n:
            problems.append(f"{split}: expected {n} tasks, found {len(tasks[split])}")
        for t in tasks[split]:
            for arm in ("B", "C"):
                for seed in SEEDS:
                    if (split, t, arm, seed) not in table:
                        problems.append(f"missing {split}/{t}/{arm}/{seed}")
    if problems:
        return dict(decision="invalid-input", problems=problems[:20])
    score = {(t, a): np.mean([table[("heldout", t, a, s)] for s in SEEDS]) for t in tasks["heldout"] for a in ("B", "C")}
    d = np.array([score[(t, "C")] - score[(t, "B")] for t in tasks["heldout"]])
    delta = float(d.mean())
    p = exact_signflip_p(d)
    lo, hi = mc_interval(d)
    fail = {a: sum(sum(1 - table[("regression", t, a, s)] for s in SEEDS) >= 2 for t in tasks["regression"]) for a in ("B", "C")}
    extra = fail["C"] - fail["B"]
    guard_ok = extra <= REGRESSION_TOLERANCE
    fabrication_ok = fabricated.get("C", 0) <= fabricated.get("B", 0)
    if delta >= THRESHOLD - 1e-12 and p < ALPHA_ONE_SIDED and guard_ok and fabrication_ok:
        decision = "adopt"
    elif delta >= THRESHOLD - 1e-12 and guard_ok and fabrication_ok:
        decision = "inconclusive-promising"
    else:
        decision = "do-not-adopt"
    return dict(
        decision=decision,
        estimand="mean over held-out tasks of (C seed-pooled acceptance - B seed-pooled acceptance)",
        delta=round(delta, 6), threshold=THRESHOLD,
        exact_one_sided_signflip_p=p, alpha_one_sided=ALPHA_ONE_SIDED,
        descriptive_95pct_interval=[lo, hi],
        task_wins_ties_losses=[int((d > 0).sum()), int((d == 0).sum()), int((d < 0).sum())],
        per_seed_acceptance={a: {str(s): float(np.mean([table[("heldout", t, a, s)] for t in tasks["heldout"]])) for s in SEEDS} for a in ("B", "C")},
        regression_majority_failures=fail, regression_extra_failures_C=extra, regression_tolerance=REGRESSION_TOLERANCE, regression_guard_passed=guard_ok,
        fabricated_claims=dict(fabricated), fabrication_guard_passed=fabrication_ok,
        per_task_difference={t: float(x) for t, x in zip(tasks["heldout"], d)},
    )


def self_test():
    # exact p against brute force on a small vector
    rng = np.random.default_rng(1)
    for n in (5, 8, 11):
        d = rng.choice([-1, -2 / 3, -1 / 3, 0, 1 / 3, 2 / 3, 1], n)
        brute = np.mean([(np.array(s) * np.abs(d)).sum() >= d.sum() - 1e-9 for s in np.array(np.meshgrid(*[[-1, 1]] * n)).T.reshape(-1, n)])
        assert abs(exact_signflip_p(d) - brute) < 1e-12, (n, exact_signflip_p(d), brute)
    # synthetic decisions
    def table_for(c_rate_by_task, b_rate=0.0, reg_c_fail=0, reg_b_fail=0):
        t = {}
        for i in range(24):
            for s_i, s in enumerate(SEEDS):
                t[("heldout", f"H{i:02}", "B", s)] = int(s_i < round(3 * b_rate))
                t[("heldout", f"H{i:02}", "C", s)] = int(s_i < c_rate_by_task(i))
        for i in range(12):
            for s in SEEDS:
                t[("regression", f"R{i:02}", "B", s)] = int(i >= reg_b_fail)
                t[("regression", f"R{i:02}", "C", s)] = int(i >= reg_c_fail)
        return t
    strong = decide(table_for(lambda i: 3 if i < 9 else 0), {})        # 9/24 tasks always accepted by C
    weak = decide(table_for(lambda i: 3 if i < 3 else 0), {})          # 3/24 -> +12.5 pp but few tasks
    harmed = decide(table_for(lambda i: 3 if i < 9 else 0, reg_c_fail=3), {})
    assert strong["decision"] == "adopt", strong
    assert weak["decision"] == "inconclusive-promising", weak
    assert harmed["decision"] == "do-not-adopt", harmed
    missing = decide({k: v for k, v in table_for(lambda i: 0).items() if k[1] != "H00"}, {})
    assert missing["decision"] == "invalid-input"
    print(json.dumps(dict(self_test="passed", strong=[strong["delta"], strong["exact_one_sided_signflip_p"]],
                          weak=[weak["delta"], weak["exact_one_sided_signflip_p"]], harmed_extra=harmed["regression_extra_failures_C"]), indent=1))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", nargs="?")
    p.add_argument("--out")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    if not a.csv:
        p.error("csv path required")
    result = decide(*load(a.csv))
    text = json.dumps(result, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    sys.exit(0 if result["decision"] != "invalid-input" else 2)


if __name__ == "__main__":
    main()
