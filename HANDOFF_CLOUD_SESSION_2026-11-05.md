# Handoff: Claude Code cloud session, November 5, 2026

Read this after `START_HERE.md`. It summarizes one cloud session: four independent analyses and a candidate-008 draft. All work is on GitHub as **draft pull requests**, and nothing is merged.

This file does not supersede `program/CURRENT_STATE.md`. Whoever merges these PRs should update `CURRENT_STATE.md` and `START_HERE.md` in the project's usual style.

## Rules that held throughout (keep them)

- **No new data was touched or created:**
  - Final/regression (EV/RG) tasks were never read, recreated or guessed.
  - No model generation, no training and no GPU work were run.
- **Additive changes only:**
  - Existing files were never modified; every PR only adds files under new folders.
  - The one exception is a shared audit script, edited inside its own new folder (see PR #4).
- **Approvals are tied to exact hashes:**
  - Every approval names an exact `SHA256.json` hash.
  - Old approvals never transfer to a new candidate.
  - `CURRENT_CANDIDATE.txt` is still `candidate-006`.

## The pull requests

| # | Title | Branch | Base | What to read first |
|---|---|---|---|---|
| [1](https://github.com/TronBronson1/qwenny-finetune-study/pull/1) | Independent audit: candidate-007 rubric mutants | `claude/c007-rubric-audit` | `main` | `independent-review/c007-rubric-audit/REPORT.md` |
| [4](https://github.com/TronBronson1/qwenny-finetune-study/pull/4) | Draft candidate-008: repair rubric gaps from the c007 audit | `claude/candidate-008` | **#1's branch** (stacked) | `studies/S010-rubric-gap-repair/RESULTS.md` |
| [2](https://github.com/TronBronson1/qwenny-finetune-study/pull/2) | Independent analysis: S009 slowdown forensics | `claude/s009-slowdown` | `main` | `independent-review/s009-slowdown/REPORT.md` |
| [3](https://github.com/TronBronson1/qwenny-finetune-study/pull/3) | Independent analysis: power of the final adoption rule | `claude/power-sim` | `main` | `independent-review/power-sim/REPORT.md`, then `PREREGISTRATION_PROPOSAL.md` |
| [6](https://github.com/TronBronson1/qwenny-finetune-study/pull/6) | Proposal: candidate-009 error-path input preservation (S011) | `claude/candidate-009` | **#4's branch** (stacked) | `studies/S011-error-path-preservation/RESULTS.md` |

**Merge order:** #1, then #4, then #6 (only if you approve candidate-009). #2 and #3 are independent. The PRs add separate folders and do not conflict with each other.

## 1. Candidate-007 rubric audit (PR #1)

**Method.**
- 1,134 single-requirement mutants were built from each unchanged reference.
- 973 of them were confirmed, in a fresh process, to differ from the reference on a concrete input.
- Both the 006 and 007 gold suites were run against the reference and every confirmed mutant: 2,090 pytest runs, plugin autoload off, with a timeout.

**Results.**
- Surviving mutants fell from **121 in 006 to 76 in 007**: 45 fixed, 0 new.
- Every previously reported gap was fixed except **TR044**. Its gold catches digit folding but not `[0-9]`→`\d`; the same gap is in TR037/041/042.

**New gap classes in 007 (findings N1–N7):**

| Finding | Gap |
|---|---|
| N1 | Non-leading non-ASCII digits are accepted |
| N2 | Ordinary wrong-type cases that untyped code also rejects (23 tasks) |
| N3 | No mixed type/value order witness |
| N4 | In-place sort is hidden because all valid inputs are already sorted |
| N5 | Boundary gaps: DV007, DV010, DV011, TR050 |
| N6 | Literal character preservation is untested |
| N7 | Error-path input mutation (contract-only) |

**Rerun:** `python3 independent-review/c007-rubric-audit/run_audit.py` (needs pytest, about 10 minutes). Add `--candidates OLD NEW --results-dir DIR` to compare any pair.

## 2. Candidate-008 draft (PR #4, study S010)

- **How it was built.**
  - The builder reuses candidate-007's own builder functions.
  - It first regenerates **911 candidate-007 files byte-identically**.
  - It then applies only the additions declared in `studies/S010-rubric-gap-repair/repair_config_008.py`, keyed to N1–N6.
- **Size.** Gold cases rose from 1,475 to **1,555**. Designated mutants rose from 407 to **463**: all 007 ids are kept, plus 56 audit mutants promoted with declared witnesses. The references are unchanged.
- **Calibration (Linux, Python 3.13, pytest 9.2).** 72/72 gold suites pass their references; 463/463 mutants are rejected at their declared witness.
- **Audit rerun 007 → 008.** Surviving mutants fell from 76 to **19**: 57 fixed, 0 new. All 19 are N7.
- **N7 deferred.** The model-visible coverage expectations only ask for before/after checks on valid calls, so fixing N7 needs a declared **prompt** revision, not just gold changes.
- **User decision, Nov 5.** The new cases and labels were reviewed and the hash `b65935295c94814fc7744f70feac49aedf809847a629961ae9bfbc75f72e18f4` approved; see `dataset-v1/USER_REVIEW_2026-11-05.json`. That approval does **not** select candidate-008 as current, export it or authorize a training run.

**Cloud gates.** `.github/workflows/s010-cloud-gates.yml` runs on every push to the branch, or manually from the Actions tab:
- **Windows validation:** runs the candidate-008 validator on `windows-latest` with Python 3.15, falling back to 3.14 with the fallback recorded. Download the `s010-windows-validation` artifact.
- **Pinned-tokenizer profile:** the tokenizer must first reproduce the committed S007 profile exactly. Download the `s010-token-profile` artifact.

**Both gates passed** in run [41957973433](https://github.com/TronBronson1/qwenny-finetune-study/actions/runs/41957973433). Job logs and the extracted JSON are in `studies/S010-rubric-gap-repair/ci-run-41957973433/`.

- **Windows validation:** Windows Server 2025, **Python 3.15.2, pytest 9.2.0**. The approved candidate hash was verified at start. 72/72 references pass (1,555 cases); 463/463 designated mutants are rejected at their declared witness.
- **Tokenizer profile:**
  - The pinned tokenizer reproduces the S007 profile exactly (60/60 rows).
  - Candidate-008 totals 63,871 chat tokens, +2.3 % over 007.
  - The maximum is **2,918 (TR058)**, the only chat over 2,048, as in 007. The next longest is TR049 at 2,021.

Optional: rerun the validation on your own PC to record that exact machine:

```bash
python studies/S010-rubric-gap-repair/validate_candidate_008.py --out studies/S010-rubric-gap-repair/validation-windows-pc
```


## 3. S009 slowdown forensics (PR #2)

- **Missing evidence.** The per-microbatch log `training-v1/runs/qwenny-003-calibrated-baseline/events.jsonl`, plus `gpu-memory.csv` and the Windows counter CSV, are git-ignored and exist only on the PC. Run this on the PC to fill the time and memory columns from them; each file is checked against its committed hash:

  ```bash
  python independent-review/s009-slowdown/s009_forensics.py --run-dir training-v1/runs/qwenny-003-calibrated-baseline
  ```

- **Evidenced:**
  - The reconstructed batch order matches the logged token totals exactly.
  - The stalled batch was TR031, a mid-length 1,188-token example.
  - PyTorch's reserved memory never grew.
  - Other GPU consumers held more memory after the run than the 8 GiB load guard allowed at its start.
  - The 1,200 s ceiling had only 6–11 % headroom even without a slowdown.
- **Best-supported explanation:** other GPU consumers took the headroom, and Windows then paged memory. This mechanism is plausible but was not measured in S009.
- **Proposed diagnostic:** C0a, C1–C5 and C0b, each changing one variable; 1,800 s per condition with a stall watchdog. Fixed telemetry is checked at startup. See REPORT §3.

## 4. Adoption-rule power simulation (PR #3)

**Findings at 24 tasks:**
- At a true +10 pp effect, the ≥10 pp threshold is met only about **45 %** of the time.
- The regression guard "≤ 1 extra failure on 12 tasks" falsely rejects a harmless adapter **18–23 %** of the time, which caps the whole rule at about 79 %.
- Tasks needed for 80 % power, at base 10 % with 3 seeds: never reached at +10 pp; 72 tasks at +15 pp; 48 at +20 pp.

**Recommended pre-registration:**
- Seed-pooled per-task paired difference as the estimand.
- Exact sign-flip permutation test, one-sided 0.025.
- Three-way decision: adopt / inconclusive / do not adopt.
- Majority-of-seeds regression guard with tolerance 2.
- An explicit expectation statement about power.

Decide this **before** any held-out evaluation, and record it as a change to `01_EXPERIMENT_PLAN.md`'s provisional rule.

## 5. Later in the same session

- **TR058 fit overlay for candidate-008 (S010).**
  - The overlay is presentation-only: AST equal to the gold, identical per-case results for the reference and all 8 mutants.
  - The pinned tokenizer measures **2,918 → 1,919 tokens**, so every candidate-008 training chat now fits within 2,048 (maximum 2,021, TR049).
  - Record: `studies/S010-rubric-gap-repair/TRAINING_FIT_OVERLAY.json`. It is not an export.
- **S009 diagnostic, ready to run (PR #2).**
  - `independent-review/s009-slowdown/diagnostic/` implements the frozen C0a, C1–C5, C0b protocol: per-condition child processes, all-process Windows GPU counters with a startup gate, a stall watchdog and an 1,800 s ceiling. `summarize.py` applies the frozen verdict.
  - The CPU dry run was rehearsed in the cloud; the GPU path has **not** run. On the PC, start with the dry run:

    ```bash
    python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --dry-run --ceiling 60 --idle 1
    ```

- **Adoption-rule pre-registration (PR #3).**
  - `PREREGISTRATION_PROPOSAL.md` contains amendment text for the plan; it needs approval **before** any held-out or regression generation.
  - `decide.py` computes the decision from a CSV of outcomes. It uses an exact sign-flip p-value, and its self-test checks that p-value against brute-force enumeration.
- **Candidate-009 proposal (PR #6, S011)** closes N7:
  - **Instruction:** one coverage sentence changes in the 19 mutable-input tasks: "Compare inputs before and after every call, including calls that raise."
  - **Gold and mutants:** every exception test now checks its inputs, and 19 audit mutants are promoted.
  - **Validation:** 482/482 mutants rejected on Windows with Python 3.15.2, and the audit rerun leaves **0 of 973** confirmed mutants surviving.
  - **Size:** 64,319 tokens in total; the TR058 overlay is 1,967 tokens.
  - **Amendment 1**, after an independent read-through review (`independent-review/case-review-008-009/`):
    - TR030 gets two real type-before-shape witnesses and a shape-first mutant, because the 008 witness e013 does not separate the two orders.
    - DV001's sentence now specifies identity comparison.
    - Three labels are renamed.
  - **After the amendment:** 1,557 cases and 483/483 mutants, passed on Windows with Python 3.15.2. The audit still shows 0 surviving mutants and none new. Total 64,384 tokens.
  - **Approval:** it needs approval of the new wording (the main sentence, the DV001 addition and the renamed labels) and of the hash `a3f1425972bb5c25e8c9579ccad71b8f5555abc49f735cbe91d677f00b5b1aeb`. The candidate-008 approval does not transfer.
- **Staged candidate-008 token packets** (`studies/S010-rubric-gap-repair/packets-008/`):
  - Built in GitHub Actions after first regenerating S009's committed baseline packets byte-for-byte.
  - Maximum training row 1,919 tokens (TR058 overlay), exact answer-only masks.
  - **Not authorized for training.** That needs your explicit authorization naming `messages_jsonl_sha256` `b3aa1c91…` and `train_jsonl_sha256` `dd2eb1a0…` (`packets-008/report.json`). The maximum example is 39 tokens longer than S009's, so repeat the GPU maximum-example preflight.
- **Independent read-through review** of the 60 new candidate-008 cases (`independent-review/case-review-008-009/` on the candidate-009 branch):
  - None contradicts its contract.
  - One is a weak witness (TR030 e013), which stays in the frozen 008 and is fixed in 009.
  - This was a fresh-context reviewer agent, not an external human.

## Open decisions and next steps (in suggested order)

1. Review and merge PRs #1 → #4 (→ #6), #2 and #3, or close any you reject. Then update `program/CURRENT_STATE.md` and `START_HERE.md`.
2. Decide whether to approve candidate-009 (new sentence + hash) or keep candidate-008. Either way, use that candidate's validated TR058 fit overlay for training packets.
3. Decide which candidate becomes current and whether it gets a training export. Both need an explicit new statement from the user.
4. N7 is handled by the candidate-009 proposal (PR #6). Rejecting it leaves N7 as a documented, deferred gap in candidate-008.
5. On the PC, run S009 forensics with `--run-dir`, then the frozen local diagnostic protocol, before any new paired training attempt.
6. Approve, or edit and then approve, `independent-review/power-sim/PREREGISTRATION_PROPOSAL.md` before held-out evaluation.

## Environment notes

- The cloud session used Python 3.13.18 and pytest 9.2.0 on Linux. The project's established runtime is Python 3.15 and pytest 9.2 on Windows.
- Hugging Face and GitHub artifact storage were blocked in the cloud session. The token profile therefore ran in GitHub Actions, and its results were read from the job logs.
- Large generated files, such as the audit's `build/` mutant sources, are git-ignored and regenerated by the scripts.
