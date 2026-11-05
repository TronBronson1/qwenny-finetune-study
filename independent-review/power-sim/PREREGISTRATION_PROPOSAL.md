# Proposed pre-registered adoption decision (amendment to `01_EXPERIMENT_PLAN.md`)

**Status:** proposal only. It takes effect only if the user approves it explicitly, and the approval must be recorded **before** any held-out (final) or regression output is generated.

`01_EXPERIMENT_PLAN.md` and `program/CURRENT_STATE.md` are not edited here. If this is approved, add the amendment below to the plan as a new dated section, and leave the original provisional rule in place as history.

The evidence for each choice is in `REPORT.md` and `TABLES.md` (power simulation, 24 held-out tasks). The reference implementation is `decide.py`.

## Why amend

The provisional rule ("C beats B by ≥ 10 pp; at most one extra regression failure") has three problems at the planned size:
- At a true +10 pp it is met only ≈45 % of the time.
- The regression clause falsely rejects a harmless adapter ≈20 % of the time.
- It leaves the seed aggregation unspecified, which `program/CURRENT_STATE.md` requires to be frozen before final evaluation.

## Amendment text (proposed)

> **Decision rule, frozen [date of approval] before any held-out or regression generation.**
>
> 1. *Data.* One first-attempt sample per held-out task × arm (B, C) × seed (17, 42, 73), using the frozen settings. Nothing is retried or selected. Token-limit stops count as not accepted.
> 2. *Per-task score.* s_ai = (number of seeds on which arm a's answer is strictly accepted) / 3.
> 3. *Estimand.* Δ = mean over the 24 held-out tasks of (s_Ci − s_Bi).
> 4. *Confirmatory test.* Exact one-sided sign-flip permutation test of Δ > 0 over all 2²⁴ sign patterns of the per-task differences. α = 0.025.
> 5. *Regression guard.* A regression task counts as failed for an arm if that arm fails on at least 2 of the 3 seeds. The guard fails if C has **3 or more** more failed regression tasks than B.
> 6. *Execution-claim guard.* The guard fails if C's answers contain more unsupported execution claims than B's, counted over all scored answers.
> 7. *Decision.*
>    - **Adopt:** Δ ≥ 0.10 **and** p < 0.025 **and** both guards pass.
>    - **Inconclusive-promising:** Δ ≥ 0.10 and both guards pass, but p ≥ 0.025. Do not adopt. A confirmation needs a newly assembled held-out set; the used set is retired from tuning.
>    - **Do not adopt:** otherwise.
> 8. *Reporting.* Report Δ, the exact p-value, a descriptive 95 % interval, task-level wins/ties/losses, per-seed acceptance by arm, regression failures by arm, and execution-claim counts, whatever the decision. `independent-review/power-sim/decide.py` (sha256 recorded at approval) computes the decision; an independent recomputation must agree.
> 9. *Expectation statement.* With 24 tasks, this rule has about 14–18 % power at a true +10 pp, 30–48 % at +15 pp and 49–78 % at +20 pp, depending on B's base rate (0–20 %). False adoption at no effect is below 2 % (0.6 % at a B base rate of 10 %, 1.4 % at 20 %). An "inconclusive" or "do not adopt" result at this size does not show that the adapter has no effect.

## Choices and what they cost (from the simulation)

| Choice | Alternative | Why |
|---|---|---|
| Seed-pooled task score | majority-of-seeds or seed 42 only | Uses all three seeds without treating them as independent tasks. Majority-of-seeds discards information (McNemar has 32 % power at +20 pp vs 59 % for the sign-flip test). |
| Exact sign-flip test | percentile bootstrap | The bootstrap is anti-conservative here (4.1 % type I error at a nominal 2.5 %). The sign-flip test is exact and deterministic. |
| Tolerance 2 on regression | the original tolerance 1 | False rejection of a harmless adapter falls from ≈20 % to ≈6–11 %. The cost: a 10 pp regression harm is caught only ≈25 % of the time, against ≈44 % at tolerance 1. Neither tolerance gives real protection with 12 tasks; enlarge the regression set if subtle regressions matter. |
| Three-way outcome | adopt / reject | Keeps the threshold practical while making the "real but unconfirmed" case visible instead of reporting it as failure. |

## Approval record template

If approved, add `program/ADOPTION_RULE_APPROVAL_<date>.json` (new file):

```json
{
  "date": "<YYYY-MM-DD>",
  "approver": "user via chat",
  "user_statement": "<verbatim>",
  "approved_text": "independent-review/power-sim/PREREGISTRATION_PROPOSAL.md#amendment-text-proposed",
  "proposal_sha256": "<sha256 of PREREGISTRATION_PROPOSAL.md>",
  "decide_py_sha256": "<sha256 of decide.py>",
  "held_out_or_regression_outputs_generated_before_approval": false
}
```

## Self-test

```bash
python independent-review/power-sim/decide.py --self-test
```

This checks the exact p-value against brute-force enumeration and the adopt / inconclusive / do-not-adopt / invalid-input paths on synthetic data. It does not use any real task data.
