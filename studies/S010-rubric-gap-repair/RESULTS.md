# S010 results — candidate-008 draft (rubric-gap repair)

Built and validated November 5, 2026, on CPU only. There was no model generation, no optimizer update and no approval or export. `CURRENT_CANDIDATE.txt`, candidate-006/007 and all earlier artifacts are unchanged.

## What changed

- **Additions:** 33 of 72 tasks gained declared gold cases; see `repair_config_008.py`.
  - 17 new normal-return cases. These add labels to the model-visible coverage list.
  - 43 new invalid cases.
  - The generator adds automatic type-before-value companion cases for the new value errors.
- **Size:** gold cases rose from 1,475 to **1,555**. The correct implementations are byte-identical to candidate-007.
- **Mutants:** designated mutants rose from 407 to **463**. All 407 candidate-007 mutants are kept with the same ids and sources, and their witnesses are refreshed. 56 independent-audit mutants are newly promoted, each with a declared witness.
- **Gaps closed:**

  | Finding | What was added |
  |---|---|
  | N1 | Non-ASCII digit in a non-leading position: TR037, TR041, TR042, TR044 |
  | N2 | Ordinary wrong types that duck-typed code accepts: a list of str for str, a tuple for list or a list for tuple, and a negative float before a domain check. Covers 23 tasks. |
  | N3 | Mixed type/value order witnesses: DV004, DV010, DV011, TR030 |
  | N4 | Unsorted valid inputs: TR029, TR030, TR033, TR034 |
  | N5 | Boundaries: DV007 `column == columns`, DV010 4/5-digit limits and a single operand, DV011 merge logic, TR050 `columns = 0` |
  | N6 | Literal character preservation and classification: TR014, TR015, TR016, TR024, TR060 |

- **Deferred:** N7, error-path input mutation (19 audit mutants, 17 tasks). The model-visible coverage expectations limit before/after checks to valid calls, so fixing it needs a declared prompt revision, not just new gold.

## Gates

| Gate | Result |
|---|---|
| Builder reproduces candidate-007 (911 code/case/prompt/mutant files) | **byte-identical** (`reproduce-007.json`) |
| Gold suites pass unchanged references, non-empty, no skips | **72/72, 1,555 cases** (`validation-001/summary.json`) |
| Every designated mutant rejected at its declared witness node | **463/463** |
| Independent audit rerun, 007 → 008 | 76 → **19** surviving mutants. 57 fixed, **0 new**. All 19 survivors are the deferred N7 family. See `independent-review/c007-rubric-audit/results-007-vs-008/`. |
| Previously reported gaps (review-002 plus the 16 list tasks) | All covered in 008 |

One audit mutant is killed by the new gold but cannot be *designated*: DV010 with the regex quantifier `{0,3}`→`{0,2}`. It rejects the valid `'9999'`, and the S007 rule gives no credit for a mutant raising on a valid input. It is listed in `build-report.json` → `still_surviving_audit_mutants`.

## Length impact (estimate)

The pinned tokenizer was not reachable from this environment. `estimate_lengths.py` scales each task's measured candidate-007 token counts by its character growth.

- Total training-chat tokens go from 62,428 to about **63,486** (+1.7 %).
- The maximum goes from 2,852 to about **2,906**, on TR058, which was already over the 2,048 budget in 007.
- No other task is estimated over 2,048.
- The largest increase is TR014, about +121 tokens.

Profile with the pinned tokenizer before training.

## Remaining gates before any training use

1. ~~Validate on Windows Python 3.15 / pytest 9.2.~~ Done in the cloud: passed on a GitHub Windows runner with Python 3.15.2 and pytest 9.2.0 (see below). An optional rerun on the user's own PC would record that exact machine.
2. ~~Profile token lengths with the pinned tokenizer.~~ Done in the cloud (see below). TR058 now has a validated fit overlay at 1,919 tokens (see below).
3. ~~Review the new cases and labels.~~ Done: the user reviewed them on November 5, 2026 (`dataset-v1/USER_REVIEW_2026-11-05.json`).
4. ~~Obtain explicit corpus approval for the new hash.~~ Done: the user approved `b65935295c94814fc7744f70feac49aedf809847a629961ae9bfbc75f72e18f4` (candidate-008 `SHA256.json`) in the same record. That approval does not select candidate-008 as current, export it or authorize a training run.
5. Decide separately whether to revise prompts for N7.

Note: the builder's docstring names `dataset-v1/candidate-007/build-sources/build_repair.py` as the reused source. The code actually loads `studies/S007-measurement-repair/build_repair.py`, because that copy's relative paths resolve correctly. The two files are byte-identical, so the docstring was left alone to keep the hashed candidate copy unchanged.

## Cloud gates (GitHub Actions run [41957973433](https://github.com/TronBronson1/qwenny-finetune-study/actions/runs/41957973433), commit `7e1e458`)

The workflow is `.github/workflows/s010-cloud-gates.yml`. Its job logs are saved in `ci-run-41957973433/`. The exact JSON outputs were extracted from the `SUMMARY_JSON:` and `PROFILE_JSON:` log lines, because artifact storage could not be reached from the authoring session.

| Gate | Result |
|---|---|
| Windows validation (windows-latest, Windows Server 2025, **Python 3.15.2, pytest 9.2.0**) | **passed**. Candidate manifest hash `b6593529…18f4` was verified at start. 72/72 references pass (1,555 cases); 463/463 designated mutants are rejected at their declared witness. File: `ci-run-41957973433/windows-validation-summary.json`. |
| Pinned-tokenizer calibration (`Qwen/Qwen3.5-9B` @ `c2022362…`, transformers 5.22.1, tokenizers 0.23.3) | Re-profiling candidate-007 **reproduces the committed S007 profile exactly** (60/60 rows) |
| Candidate-008 token profile | Total 62,428 → **63,871** (+1,443, +2.3 %). Maximum **2,918** (TR058, +66); **TR058 is the only chat over 2,048**, as in 007. The next longest is TR049 at 2,021, unchanged. The largest increases are TR014 +175, TR030 +118, TR042 +106, TR044 +104, TR050 +103 and TR041 +98. File: `ci-run-41957973433/token-profile-008.json`. |

The offline estimate above (63,486 total, maximum ≈2,906) is superseded by these measured values.

## TR058 fit overlay (same method as S007 length-preview-002)

`build_tr058_overlay.py` writes `tr058-fit-overlay/`, a presentation-only version of the candidate-008 TR058 answer: pytest display ids removed, whitespace compacted, prose shortened.

- **Same tests:** the executable AST equals the candidate-008 gold, ignoring only display ids. Per-test-case results are identical for the reference and all 8 designated mutants.
- **Measured fit:** the pinned tokenizer measured it in Actions run [41958509654](https://github.com/TronBronson1/qwenny-finetune-study/actions/runs/41958509654): **2,918 → 1,919 tokens**. With the overlay, the longest full training chat is **2,021 (TR049)**, so all 60 fit within 2,048. That run also repeated the Windows validation: passed again on Python 3.15.2.
- **Record:** `TRAINING_FIT_OVERLAY.json`. Candidate-008 files are unchanged. The overlay is not an export, and training still needs explicit export authorization, mask/decode checks and a maximum-example forward/backward check, as in S009.
