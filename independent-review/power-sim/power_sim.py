#!/usr/bin/env python3
"""Monte-Carlo power analysis of the provisional final adoption rule.

Rule under test (01_EXPERIMENT_PLAN.md, program/CURRENT_STATE.md):
  adapter arm C beats prompted arm B by >= 10 percentage points in strict task
  acceptance on 24 held-out tasks (one sample per task/arm/seed, seeds 17/42/73),
  and C adds at most one failed regression task (of 12) compared with B.

Model
  * task i has a shared latent difficulty u_i ~ N(0, sigma^2) on the logit scale;
    arm a in {B, C} has per-task success probability p_ia = expit(mu_a + u_i);
    mu_B, mu_C are solved so the task-population means equal base and base+delta.
    base == 0 means arm B never succeeds (the current strict-acceptance situation).
  * seed correlation rho: within a task/arm, the per-seed success probability is
    q_ia ~ Beta with mean p_ia and intraclass correlation rho; seeds are Bernoulli(q_ia).
    rho = 0: seeds independent given the task; rho -> 1: all seeds agree.
  * one sample per task/arm/seed; arms are independent given the task.

Only numpy, scipy and matplotlib are used. Everything is seeded: rerun with
    python3 independent-review/power-sim/power_sim.py
(--quick for a smoke run). Outputs: results.json and figures/*.png next to this file.
"""
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy import optimize, special, stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
SEED = 20261105
THRESHOLD = 0.10
ALPHA = 0.05
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(80)
GH_W = GH_W / GH_W.sum()


# ---------------------------------------------------------------------------
def mean_expit(mu, sigma):
    return float(np.sum(GH_W * special.expit(mu + sigma * GH_X)))


def solve_mu(target, sigma):
    if target <= 0:
        return -np.inf
    if target >= 1:
        return np.inf
    return optimize.brentq(lambda m: mean_expit(m, sigma) - target, -40, 40)


def seed_probs(rng, p, rho, shape_seeds):
    """Per-seed success probability with intraclass correlation rho (Beta mixing)."""
    if rho <= 0:
        return p
    p = np.clip(p, 0, 1)
    k = (1 - rho) / rho
    a, b = np.maximum(p * k, 1e-12), np.maximum((1 - p) * k, 1e-12)
    q = rng.beta(a, b)
    q = np.where(p <= 0, 0.0, np.where(p >= 1, 1.0, q))
    return q


def simulate_arms(rng, reps, n_tasks, seeds, base, delta, rho, sigma):
    """Return boolean arrays B, C with shape (reps, n_tasks, seeds)."""
    u = rng.normal(0, sigma, (reps, n_tasks))
    pb = special.expit(solve_mu(base, sigma) + u) if base > 0 else np.zeros_like(u)
    pc = special.expit(solve_mu(base + delta, sigma) + u) if base + delta > 0 else np.zeros_like(u)
    out = []
    for p in (pb, pc):
        q = seed_probs(rng, p, rho, seeds)
        out.append(rng.random((reps, n_tasks, seeds)) < q[..., None])
    return out


def exact_two_sided(k_pos, k_neg):
    """Exact two-sided binomial (sign / McNemar) p-value; 1.0 when no discordant pairs."""
    n = k_pos + k_neg
    low = np.minimum(k_pos, k_neg)
    p = np.where(n > 0, np.minimum(1.0, 2 * stats.binom.cdf(low, np.maximum(n, 1), 0.5)), 1.0)
    return p


def bootstrap_lower(rng, d, boots, level=0.95, chunk=250):
    """Percentile task-cluster bootstrap lower/upper bounds for mean(d) per replicate."""
    reps, n = d.shape
    lo = np.empty(reps); hi = np.empty(reps)
    q = (1 - level) / 2
    for start in range(0, reps, chunk):
        block = d[start:start + chunk]
        idx = rng.integers(0, n, (block.shape[0], boots, n))
        means = block[np.arange(block.shape[0])[:, None, None], idx].mean(2)
        lo[start:start + chunk] = np.quantile(means, q, axis=1)
        hi[start:start + chunk] = np.quantile(means, 1 - q, axis=1)
    return lo, hi


def signflip_p(rng, d, flips, chunk=250):
    """Two-sided Monte-Carlo sign-flip (paired permutation) p-value for mean(d) per replicate."""
    reps, n = d.shape
    out = np.empty(reps)
    obs = np.abs(d.mean(1))
    for start in range(0, reps, chunk):
        block = d[start:start + chunk]
        signs = rng.choice(np.array([-1.0, 1.0]), size=(block.shape[0], flips, n))
        null = np.abs((signs * block[:, None, :]).mean(2))
        out[start:start + chunk] = (1 + (null >= obs[start:start + chunk, None] - 1e-12).sum(1)) / (flips + 1)
    return out


def evaluate(rng, B, C, boots):
    """All decision statistics for one design; returns dict of boolean arrays."""
    seeds = B.shape[2]
    pooled_diff = C.mean((1, 2)) - B.mean((1, 2))
    need = seeds // 2 + 1
    mb, mc = B.sum(2) >= need, C.sum(2) >= need
    majority_diff = mc.mean(1) - mb.mean(1)
    d = C.mean(2) - B.mean(2)                      # per-task paired difference of seed means
    mcnemar_p = exact_two_sided((mc & ~mb).sum(1), (mb & ~mc).sum(1))
    sign_p = exact_two_sided((d > 0).sum(1), (d < 0).sum(1))
    out = {
        "rule_pooled": pooled_diff >= THRESHOLD - 1e-9,
        "rule_majority": majority_diff >= THRESHOLD - 1e-9,
        "rule_seed42_only": (C[:, :, 0].mean(1) - B[:, :, 0].mean(1)) >= THRESHOLD - 1e-9,
        "mcnemar_majority": (mcnemar_p < ALPHA) & (majority_diff > 0),
        "sign_test": (sign_p < ALPHA) & (d.mean(1) > 0),
        "pooled_diff": pooled_diff,
    }
    if boots:
        lo, hi = bootstrap_lower(rng, d, boots)
        out["bootstrap_lower_gt0"] = lo > 0
        perm = signflip_p(rng, d, boots)
        out["signflip_permutation"] = (perm < ALPHA) & (d.mean(1) > 0)
        out["rule_pooled_and_signflip"] = out["rule_pooled"] & out["signflip_permutation"]
        out["rule_pooled_and_ci"] = out["rule_pooled"] & (lo > 0)
        out["ci_width"] = hi - lo
    return out


def regression_guard(rng, reps, seeds, pass_rate, harm, rho, sigma, n_tasks=12):
    """Probability that the guard rejects C. harm = true drop in mean pass rate for C."""
    fail_b, fail_c = simulate_arms(rng, reps, n_tasks, seeds, 1 - pass_rate, harm, rho, sigma)
    need = seeds // 2 + 1
    extra_single = fail_c[:, :, 0].sum(1) - fail_b[:, :, 0].sum(1)
    extra_majority = (fail_c.sum(2) >= need).sum(1) - (fail_b.sum(2) >= need).sum(1)
    extra_pooled = (fail_c.sum((1, 2)) - fail_b.sum((1, 2))) / seeds
    res = {
        # alternative tolerances (extra failures allowed) for the same aggregations
        **{f"single_seed_tol{t}": extra_single > t for t in (2, 3)},
        **{f"majority_tol{t}": extra_majority > t for t in (2, 3)},
        **{f"pooled_tol{t}": extra_pooled > t + 1e-9 for t in (2, 3)},
        # guard applied to one sample per task (seed 42 only)
        "single_seed": (fail_c[:, :, 0].sum(1) - fail_b[:, :, 0].sum(1)) > 1,
        # majority-of-seeds task failure
        "majority": ((fail_c.sum(2) >= need).sum(1) - (fail_b.sum(2) >= need).sum(1)) > 1,
        # pooled failures expressed in task units (failures / seeds)
        "pooled_task_units": (fail_c.sum((1, 2)) - fail_b.sum((1, 2))) / seeds > 1 + 1e-9,
        # literal reading: at most one extra failure in EVERY seed
        "every_seed": ((fail_c.sum(1) - fail_b.sum(1)) > 1).any(1),
    }
    return {k: float(v.mean()) for k, v in res.items()}


# ---------------------------------------------------------------------------
def run(args):
    rng = np.random.default_rng(SEED)
    reps, boots = args.reps, args.boots
    sigma, rho_default = args.sigma, 0.5
    results = {"meta": {"seed": SEED, "reps": reps, "boots": boots, "sigma_logit": sigma,
                        "threshold": THRESHOLD, "alpha_two_sided": ALPHA,
                        "numpy": np.__version__, "scipy": __import__("scipy").__version__,
                        "matplotlib": matplotlib.__version__}}
    bases = [0.0, 0.02, 0.05, 0.10, 0.20, 0.30, 0.40]
    deltas = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    rhos = [0.0, 0.5, 0.9]

    # 1. Main grid at the planned 24 tasks.
    grid = []
    for seeds in (1, 3):
        for rho in (rhos if seeds == 3 else [0.0]):
            for base in bases:
                for delta in deltas:
                    if base + delta > 0.95:
                        continue
                    B, C = simulate_arms(rng, reps, 24, seeds, base, delta, rho, sigma)
                    ev = evaluate(rng, B, C, boots if (rho == rho_default or seeds == 1) else 0)
                    row = {"n_tasks": 24, "seeds": seeds, "rho": rho, "base": base, "delta": delta}
                    for k, v in ev.items():
                        if k in ("pooled_diff", "ci_width"):
                            row[k + "_mean"] = float(np.mean(v)); row[k + "_sd"] = float(np.std(v))
                        else:
                            row["p_" + k] = float(np.mean(v))
                    grid.append(row)
        print(f"grid seeds={seeds} done", flush=True)
    results["grid_24_tasks"] = grid

    # 2. Sensitivity to task heterogeneity at base 0.10.
    sens = []
    for sig in (0.0, 0.75, 1.5, 2.5):
        for delta in (0.0, 0.10, 0.20):
            B, C = simulate_arms(rng, reps, 24, 3, 0.10, delta, rho_default, sig)
            ev = evaluate(rng, B, C, 0)
            sens.append({"sigma": sig, "delta": delta, **{"p_" + k: float(np.mean(v)) for k, v in ev.items() if k != "pooled_diff"}})
    results["sigma_sensitivity"] = sens

    # 3. Regression guard false rejection (no true harm) and detection (true harm).
    guard = []
    for seeds in (1, 3):
        for rho in ((0.0,) if seeds == 1 else (0.0, 0.5, 0.9)):
            for pass_rate in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
                for harm in (0.0, 0.10, 0.20):
                    if 1 - pass_rate + harm > 0.99:
                        continue
                    g = regression_guard(rng, reps, seeds, pass_rate, harm, rho, sigma)
                    guard.append({"seeds": seeds, "rho": rho, "pass_rate": pass_rate, "harm": harm, **g})
    results["regression_guard"] = guard
    print("guard done", flush=True)

    # 4. Tasks needed for 80 % power.
    ns = [12, 24, 36, 48, 72, 96, 128, 160, 200, 256, 320, 400, 500]
    criteria = ["rule_pooled", "mcnemar_majority", "sign_test", "bootstrap_lower_gt0", "rule_pooled_and_ci", "signflip_permutation", "rule_pooled_and_signflip"]
    curves, needed = [], []
    for base in (0.0, 0.10, 0.20):
        for delta in (0.10, 0.15, 0.20):
            for seeds in (1, 3):
                found = {c: None for c in criteria}
                for n in ns:
                    B, C = simulate_arms(rng, args.reps_n, n, seeds, base, delta, rho_default, sigma)
                    ev = evaluate(rng, B, C, args.boots_n)
                    point = {"base": base, "delta": delta, "seeds": seeds, "n_tasks": n}
                    for c in criteria:
                        point["p_" + c] = float(np.mean(ev[c]))
                        if found[c] is None and point["p_" + c] >= 0.80:
                            found[c] = n
                    curves.append(point)
                needed.append({"base": base, "delta": delta, "seeds": seeds, "rho": rho_default,
                               **{c: found[c] for c in criteria}})
                print(f"n-search base={base} delta={delta} seeds={seeds}: {found}", flush=True)
    results["power_vs_tasks"] = curves
    results["tasks_for_80_percent_power"] = needed
    results["tasks_for_80_percent_power_note"] = ("Smallest grid value in %s reaching >=0.80; None means not reached by %d tasks. "
                                                  "rho=%.1f, sigma=%.2f." % (ns, ns[-1], rho_default, sigma))

    # 5. Graded secondary endpoint: per-task k=4 fixed-input values (S008 style, ~65 % accuracy).
    graded = []
    for delta in (0.0, 0.05, 0.10, 0.15):
        for n in (8, 12, 24):
            u = rng.normal(0, 1.0, (reps, n))
            pb = special.expit(solve_mu(0.65, 1.0) + u)
            pc = special.expit(solve_mu(0.65 + delta, 1.0) + u)
            sb = rng.binomial(4, pb) / 4
            sc = rng.binomial(4, pc) / 4
            d = sc - sb
            sign_p = exact_two_sided((d > 0).sum(1), (d < 0).sum(1))
            t_p = stats.ttest_rel(sc, sb, axis=1).pvalue
            graded.append({"delta": delta, "n_tasks": n,
                           "p_sign_test": float(np.mean((sign_p < ALPHA) & (d.mean(1) > 0))),
                           "p_paired_t": float(np.nanmean((t_p < ALPHA) & (d.mean(1) > 0))),
                           "p_mean_diff_ge_10pp": float(np.mean(d.mean(1) >= THRESHOLD - 1e-9))})
    results["graded_endpoint"] = graded
    return results


# ---------------------------------------------------------------------------
def pick(rows, **kw):
    return [r for r in rows if all(abs(r[k] - v) < 1e-9 if isinstance(v, float) else r[k] == v for k, v in kw.items())]


def plots(res):
    FIG.mkdir(exist_ok=True)
    grid = res["grid_24_tasks"]
    colors = plt.cm.viridis(np.linspace(0, 0.9, 7))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, (seeds, rho) in zip(axes, ((1, 0.0), (3, 0.5))):
        for color, base in zip(colors, (0.0, 0.02, 0.05, 0.10, 0.20, 0.30, 0.40)):
            rows = sorted(pick(grid, seeds=seeds, rho=rho, base=base), key=lambda r: r["delta"])
            ax.plot([100 * r["delta"] for r in rows], [r["p_rule_pooled"] for r in rows], "o-", color=color, label=f"B base {base:.0%}")
        ax.axhline(0.8, ls=":", c="grey"); ax.axvline(10, ls="--", c="grey")
        ax.set_title(f"{seeds} seed{'s' if seeds > 1 else ''}" + (f", seed ICC {rho}" if seeds > 1 else "") + ", 24 tasks")
        ax.set_xlabel("true effect C - B (percentage points)")
    axes[0].set_ylabel("P(observed C - B >= 10 pp)")
    axes[1].legend(fontsize=8)
    fig.suptitle("Adoption threshold alone: probability the >=10 pp rule is met")
    fig.tight_layout(); fig.savefig(FIG / "rule_probability.png", dpi=150); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    labels = {"p_rule_pooled": "rule: pooled diff >= 10 pp", "p_rule_majority": "rule: majority-of-seeds diff >= 10 pp",
              "p_mcnemar_majority": "McNemar exact (majority)", "p_sign_test": "sign test (seed means)",
              "p_bootstrap_lower_gt0": "bootstrap 95% CI > 0", "p_rule_pooled_and_ci": "rule AND CI > 0",
              "p_signflip_permutation": "sign-flip permutation", "p_rule_pooled_and_signflip": "rule AND sign-flip p < .05"}
    for ax, base in zip(axes, (0.0, 0.10)):
        rows = sorted(pick(grid, seeds=3, rho=0.5, base=base), key=lambda r: r["delta"])
        for key, label in labels.items():
            ax.plot([100 * r["delta"] for r in rows], [r[key] for r in rows], "o-", label=label)
        ax.axhline(0.8, ls=":", c="grey"); ax.axhline(0.05, ls=":", c="red")
        ax.set_title(f"24 tasks x 3 seeds, B base {base:.0%}, seed ICC 0.5"); ax.set_xlabel("true effect (pp)")
    axes[0].set_ylabel("probability of a positive decision"); axes[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "power_by_test.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for seeds, rho, style in ((1, 0.0, "s-"), (3, 0.0, "o-"), (3, 0.5, "o--"), (3, 0.9, "o:")):
        rows = sorted(pick(grid, seeds=seeds, rho=rho, delta=0.0), key=lambda r: r["base"])
        ax.plot([100 * r["base"] for r in rows], [r["p_rule_pooled"] for r in rows], style, label=f"{seeds} seed(s), ICC {rho}")
    ax.set_xlabel("common acceptance rate (no true effect), %"); ax.set_ylabel("false adoption P(diff >= 10 pp)")
    ax.set_title("False adoption at zero effect, 24 tasks (threshold only)"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "false_adoption.png", dpi=150); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, harm in zip(axes, (0.0, 0.10)):
        for seeds, rho, key, style in ((1, 0.0, "single_seed", "s-"), (3, 0.5, "majority", "o-"), (3, 0.5, "pooled_task_units", "o--"), (3, 0.5, "every_seed", "o:")):
            rows = sorted(pick(res["regression_guard"], seeds=seeds, rho=rho, harm=harm), key=lambda r: r["pass_rate"])
            ax.plot([100 * r["pass_rate"] for r in rows], [r[key] for r in rows], style, label=f"{key} ({seeds} seed{'s' if seeds > 1 else ''})")
        ax.set_xlabel("B regression pass rate, %"); ax.set_title("no true harm: false rejection" if harm == 0 else "true harm 10 pp: detection")
    axes[0].set_ylabel("P(guard rejects C)"); axes[0].legend(fontsize=7)
    fig.suptitle("Regression guard: > 1 extra failure on 12 tasks")
    fig.tight_layout(); fig.savefig(FIG / "regression_guard.png", dpi=150); plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
    for ax, delta in zip(axes, (0.10, 0.15, 0.20)):
        for key, label in (("p_rule_pooled", "rule (pooled >= 10 pp)"), ("p_sign_test", "sign test"), ("p_mcnemar_majority", "McNemar (majority)"),
                           ("p_bootstrap_lower_gt0", "bootstrap CI > 0"), ("p_rule_pooled_and_ci", "rule AND CI > 0"),
                           ("p_signflip_permutation", "sign-flip permutation"), ("p_rule_pooled_and_signflip", "rule AND sign-flip")):
            rows = sorted(pick(res["power_vs_tasks"], base=0.10, delta=delta, seeds=3), key=lambda r: r["n_tasks"])
            ax.plot([r["n_tasks"] for r in rows], [r[key] for r in rows], "o-", label=label)
        ax.axhline(0.8, ls=":", c="grey"); ax.axvline(24, ls="--", c="grey"); ax.set_xscale("log")
        ax.set_title(f"+{delta * 100:.0f} pp, base 10%, 3 seeds"); ax.set_xlabel("held-out tasks")
    axes[0].set_ylabel("power"); axes[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "power_vs_tasks.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for rho in (0.0, 0.5, 0.9):
        rows = sorted(pick(grid, seeds=3, rho=rho, base=0.10), key=lambda r: r["delta"])
        ax.plot([100 * r["delta"] for r in rows], [r["p_sign_test"] for r in rows], "o-", label=f"3 seeds, ICC {rho}")
    rows = sorted(pick(grid, seeds=1, rho=0.0, base=0.10), key=lambda r: r["delta"])
    ax.plot([100 * r["delta"] for r in rows], [r["p_sign_test"] for r in rows], "s--", c="k", label="1 seed")
    ax.axhline(0.8, ls=":", c="grey"); ax.set_xlabel("true effect (pp)"); ax.set_ylabel("sign-test power")
    ax.set_title("Seed correlation erodes the value of extra seeds (24 tasks, base 10%)"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "seed_correlation.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for n in (8, 12, 24):
        rows = sorted(pick(res["graded_endpoint"], n_tasks=n), key=lambda r: r["delta"])
        ax.plot([100 * r["delta"] for r in rows], [r["p_paired_t"] for r in rows], "o-", label=f"{n} tasks, paired t")
    ax.axhline(0.8, ls=":", c="grey"); ax.set_xlabel("true effect on per-value accuracy (pp)"); ax.set_ylabel("power")
    ax.set_title("Graded secondary endpoint (4 values/task, base ~65%)"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "graded_endpoint.png", dpi=150); plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="small smoke run")
    args = parser.parse_args()
    args.sigma = 1.5
    args.reps, args.boots, args.reps_n, args.boots_n = (400, 200, 300, 150) if args.quick else (4000, 500, 1500, 300)
    start = time.time()
    res = run(args)
    res["meta"]["elapsed_seconds"] = round(time.time() - start, 1)
    out = HERE / ("results-quick.json" if args.quick else "results.json")
    out.write_text(json.dumps(res, indent=1))
    plots(res)
    if not args.quick:
        import make_tables
        make_tables.main()
    print(f"wrote {out} in {res['meta']['elapsed_seconds']} s")


if __name__ == "__main__":
    main()
