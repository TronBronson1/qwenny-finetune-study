# Independent analysis: power of the final adoption rule

**Rule tested** (`01_EXPERIMENT_PLAN.md`, `program/CURRENT_STATE.md`):

- the adapter arm **C** must beat the prompted arm **B** by **≥ 10 percentage points** in strict task acceptance on **24 held-out tasks**, with one sample per task/arm/seed and seeds 17/42/73;
- **and** C must add **at most one extra failure on 12 regression tasks**.

The third clause, fabricated execution claims, is not simulated. The plan leaves the seed aggregation open, so several readings are compared below.

**Rerun:**

```bash
python3 independent-review/power-sim/power_sim.py
```

It uses only numpy, scipy and matplotlib, with seed `20261105`, and takes ≈9 minutes on one core. `--quick` gives a smoke run. Outputs: `results.json`, `TABLES.md` (every number quoted here) and `figures/*.png`. No repository file was modified, and no held-out or regression content was read.

## Model

- **Tasks.** Each task has a shared latent difficulty u ~ N(0, 1.5²) on the logit scale, with p_arm = expit(μ_arm + u). μ_B and μ_C are solved so the task-population means equal *base* and *base + effect*. Because difficulty is shared, the design is paired: a hard task is hard for both arms.
- **Ranges.** B base rates are 0, 2, 5, 10, 20, 30 and 40 %. Base 0 means B never succeeds, which matches today's ≈0 % strict acceptance. True effects run from 0 to 30 pp.
- **Seeds.** Within a task/arm, seed success probabilities are Beta-mixed with intraclass correlation (ICC) 0, 0.5 or 0.9. ICC 0 means seeds are independent given the task; ICC 0.9 means seeds nearly always agree. Designs with 1 seed and 3 seeds are compared.
- **Size.** 4,000 replicates per cell, with 500 bootstrap and sign-flip resamples per replicate. For the task-count search: 1,500 replicates and 300 resamples. Monte-Carlo SE ≤ 0.8 pp.
- **Regression set.** 12 tasks with B pass rates of 50 to 95 %, a true harm of 0, 10 or 20 pp, and the same latent-difficulty and seed model.
- **Decision statistics** (task is the unit throughout):
  - *Rule (pooled)*: seed-pooled acceptance difference ≥ 10 pp.
  - *Rule (majority)*: task accepted on ≥ 2 of 3 seeds.
  - *Seed 42 only*.
  - *Exact McNemar* on majority-of-seeds task outcomes.
  - *Exact sign test* and *sign-flip permutation test* on per-task seed-mean differences, two-sided α = 0.05 and positive direction.
  - *Percentile task-cluster bootstrap*: 95 % CI lower bound > 0.

## Results at the planned 24 tasks

### 1. The ≥ 10 pp threshold is a coin flip at a true +10 pp effect

| True effect | P(rule met), 3 seeds, B base 0 % | B base 10 % | B base 20 % | 1 seed, B base 10 % |
|---:|---:|---:|---:|---:|
| 0 (false adoption) | 0.0 % | 5.8 % | 10.6 % | 9.2 % |
| +10 pp | 43.9 % | 47.3 % | 48.6 % | 47.5 % |
| +15 pp | 75.1 % | 72.7 % | 70.1 % | 68.8 % |
| +20 pp | 93.0 % | 87.1 % | 85.8 % | 83.9 % |
| +30 pp | 99.5 % | 98.8 % | 98.0 % | 96.8 % |

These are for the threshold clause alone, seed-pooled, ICC 0.5; see `figures/rule_probability.png`. The standard deviation of the observed difference is 5 to 10 pp, as large as the threshold itself. At a true effect equal to the threshold, the rule is met about half the time whatever the design. Reaching 80 % needs a true effect of roughly **+16 to +20 pp**.

Three seeds instead of one change little:

- they cut false adoption at base 10–20 % (9.2 → 5.8 %, 15.0 → 10.6 %);
- they add only 2–10 pp of power for effects ≥ 15 pp;
- they matter less as the seed ICC rises (`figures/seed_correlation.png`).

Three seeds are not three independent tasks.

### 2. Adding the regression guard caps the whole rule at about 79 %

"At most one extra failure on 12 tasks" falsely rejects a truly harmless adapter **18 to 23 % of the time** when regression pass rates are 50 to 80 %. It does so 11 % at 90 % and ≈5 % at 95 % (`figures/regression_guard.png`).

The guard still detects a true 10 pp regression harm only **37 to 45 %** of the time. The literal reading "≤ 1 extra in *every* seed" is worse: 36 to 43 % false rejection at ICC 0.5.

| Full rule = threshold × guard (B regression pass rate 70 %, 3 seeds, majority guard) | B base 0 % | 10 % | 20 % |
|---|---:|---:|---:|
| False adoption, no effect | 0.0 % | 4.5 % | 8.4 % |
| P(adopt), +10 pp | 34.7 % | 37.4 % | 38.5 % |
| P(adopt), +20 pp | 73.6 % | 68.9 % | 67.8 % |
| P(adopt), +30 pp | 78.7 % | 78.1 % | 77.5 % |

### 3. Formal tests are underpowered at 24 tasks

Three seeds, ICC 0.5, `figures/power_by_test.png`:

| Test | Type I error (base 10 %) | Power +10 pp | +15 pp | +20 pp |
|---|---:|---:|---:|---:|
| Exact McNemar (majority) | 0.1 % | 5.5 % | 15.8 % | 31.9 % |
| Exact sign test | 0.7 % | 14.3 % | 30.9 % | 50.9 % |
| Sign-flip permutation | 0.8 % | 18.1 % | 36.4 % | 58.5 % |
| Bootstrap 95 % CI > 0 | 4.1 % | 32.9 % | 55.1 % | 72.9 % |

The bootstrap gains its power by being **anti-conservative**: 4.1 % type I against a nominal 2.5 % one-sided, rising further when few tasks have any success. It should not be the confirmatory test.

McNemar on majority-collapsed outcomes discards information and is the weakest option. The sign-flip permutation test is valid and conservative here, and it uses seed-mean magnitudes.

### 4. Tasks needed for 80 % power

Three seeds, ICC 0.5. The smallest count on the grid 12/24/36/48/72/96/128/160/200/256/320/400/500:

| B base | Effect | Threshold alone | Sign-flip permutation | Sign test | McNemar | **Threshold AND sign-flip** |
|---:|---:|---:|---:|---:|---:|---:|
| 0 % | +10 pp | never (≈50 %) | 72 | 72 | 96 | never |
| 0 % | +15 pp | 36 | 36 | 36 | 72 | **48** |
| 0 % | +20 pp | 12 | 36 | 36 | 48 | **36** |
| 10 % | +10 pp | never | 128 | 128 | 200 | never |
| 10 % | +15 pp | 48 | 72 | 72 | 96 | **72** |
| 10 % | +20 pp | 12 | 48 | 48 | 72 | **48** |
| 20 % | +10 pp | never | 200 | 200 | 256 | never |
| 20 % | +15 pp | 72 | 96 | 96 | 128 | **96** |
| 20 % | +20 pp | 24 | 48 | 72 | 72 | **48** |

With one seed, the counts rise by about 1.3 to 2×; see `TABLES.md`. A rule requiring an observed ≥ 10 pp *and* significance can never reach 80 % power at a true +10 pp: half of all true-+10 pp outcomes fall below the threshold.

### 5. Other checks

- **Heterogeneity.** Varying task heterogeneity (logit SD 0 to 2.5) moves the threshold probability by ≤ 5 pp; see `TABLES.md`. It moves sign-test power at +20 pp by up to 15 pp, from 44 % to 59 %. The conclusions do not depend on that assumption.
- **Graded endpoint.** A secondary endpoint scored per value, S008-style (4 values per task, base ≈ 65 %, one seed), is **not** a power rescue at 24 tasks: the paired t-test has 37 % power at +10 pp and 68 % at +15 pp. Per-item noise with 4 items per task is as large as the strict-acceptance noise. It is useful as a mechanism measure, not as the decision endpoint.

## Recommendation: pre-registerable aggregation

Freeze the following before any held-out evaluation.

1. **Unit and estimand.**
   - The held-out task is the unit.
   - For each task i and arm a: s_ai = (strictly accepted seeds among 17/42/73) / 3. There is one sample per task/arm/seed and no best-of selection.
   - The primary estimand is Δ = mean_i (s_Ci − s_Bi), the seed-pooled paired difference.
   - Report Δ with task-level wins/ties/losses and per-seed rates.
2. **Confirmatory test.**
   - Exact sign-flip permutation test on the 24 values d_i = s_Ci − s_Bi, one-sided α = 0.025 (equivalently two-sided 0.05 with positive direction). Enumerate all 2²⁴ sign patterns, or use ≥ 100,000 Monte-Carlo flips with a fixed seed.
   - Report a 95 % interval by test inversion, or the sign-flip interval. Use a percentile bootstrap only as a descriptive figure.
3. **Three-way decision.**
   - **Adopt**: Δ ≥ 10 pp **and** permutation p < 0.025 **and** the regression guard passes.
   - **Inconclusive, promising**: Δ ≥ 10 pp but p ≥ 0.025. Collect a fresh held-out set; do not reuse this one for tuning.
   - **Do not adopt**: otherwise.
4. **Regression guard.**
   - Use majority-of-seeds task failures.
   - Fail the guard only if C has **≥ 3 more failed tasks than B (tolerance 2)**. This gives 6 to 11 % false rejection at pass rates 50 to 80 %, against ≈20 % at tolerance 1.
   - State plainly that 12 tasks detect a 10 pp harm only ≈25 % of the time. The guard catches gross breakage, not subtle regression. If subtle regression matters, enlarge the regression set rather than tighten the tolerance.
5. **Expectation statement**, to put in the pre-registration. With 24 tasks this procedure (threshold AND permutation) has ≈14 to 18 % power at a true +10 pp, ≈30 to 48 % at +15 pp and ≈49 to 78 % at +20 pp, for B base rates of 20 % down to 0 %. Detecting +15 pp at 80 % needs ≈48 to 96 tasks; +10 pp needs ≈72 to 200.
6. **Seeds.** Keep 3 seeds as variability measurement, but do not count them as replication. When planning the next evaluation, prefer more held-out tasks over more seeds.

Since today's strict acceptance is near 0 %, false adoption is not the main risk. The main risk is a *real* modest improvement being reported as a failure, or as a +10 pp "win" that is mostly noise. The three-way decision and the expectation statement make both visible ahead of time.

## Limitations

- The logit-normal difficulty, the Beta seed model and arm independence given the task are assumptions. Real C−B correlation could differ; sensitivity to heterogeneity is small for the threshold and moderate for the tests.
- The clause on fabricated execution claims is not modelled.
- The effect is assumed homogeneous on the logit scale and measured as a population-mean difference. Effects concentrated in a few task families would behave differently.
- Grid search over task counts uses discrete steps; the reported value is the first grid point reaching 80 %.

## Figures

- `rule_probability.png`: P(≥ 10 pp) against true effect, by base rate, for 1 vs 3 seeds.
- `power_by_test.png`: every decision statistic against effect, at base 0 % and 10 %.
- `false_adoption.png`: zero-effect adoption against base rate and seed ICC.
- `regression_guard.png`: false rejection and harm detection for the guard readings.
- `power_vs_tasks.png`: power against held-out task count for +10/+15/+20 pp.
- `seed_correlation.png`: sign-test power by seed ICC.
- `graded_endpoint.png`: per-value secondary endpoint.
