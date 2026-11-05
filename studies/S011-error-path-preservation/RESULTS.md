# S011 results — candidate-009 proposal (error-path input preservation)

Built November 5, 2026, on CPU only. Candidate-009 is a **proposal**: it changes one model-visible sentence in 19 tasks, so it needs explicit user approval of that sentence and of its hash. Candidate-008 and its approval are unchanged.

## Change

- **Instruction:** in the 19 mutable-input tasks, "Compare valid inputs before and after calls." becomes "Compare inputs before and after every call, including calls that raise."
- **Gold:** every expected-exception test snapshots its arguments and asserts they are unchanged. TARGET.md and the training packets carry the new gold and the updated preservation sentence.
- **Mutants:** the 19 audit `mutation-error` mutants are promoted to designated mutants, R-ids continuing per task. Each was hash-checked against the audit, and each witness is an invalid case where the expected exception is raised but an argument changed. The 463 candidate-008 mutants are unchanged.
- **Unchanged:** the other 53 tasks, all references, cases and oracle files.

## Gates

| Gate | Result |
|---|---|
| Gold vs unchanged references | 72/72, 1,555 cases (Linux, Python 3.13, pytest 9.2; `validation-001/summary.json`) |
| Designated mutants rejected at their declared witness | **482/482** (463 + 19) |
| Independent audit, 008 → 009 | 19 → **0** surviving confirmed mutants, out of 973; **0 new** (`independent-review/c007-rubric-audit/results-008-vs-009/`) |
| TR058 fit overlay rebuilt for 009 | AST equal ignoring display ids; per-case results identical for reference + 9 variants; **2,957 → 1,967 tokens** (`TRAINING_FIT_OVERLAY.json`) |
| Windows validation (GitHub runner, **Python 3.15.2, pytest 9.2.0**), run [41960481296](https://github.com/TronBronson1/qwenny-finetune-study/actions/runs/41960481296) | **passed**: hash `fa1c0e58…` verified, 72/72 suites, 1,555 cases, 482/482 mutants |
| Pinned-tokenizer profile, same run | Reproduces S007 exactly. Total 62,428 (007) → **64,319** (+3.0 %); 008 was 63,871. Only TR058 is over 2,048 (2,957); with the overlay, the maximum full training chat is **2,021** (TR049). |

Candidate hash (`SHA256.json`) **after amendment 1**: `a3f1425972bb5c25e8c9579ccad71b8f5555abc49f735cbe91d677f00b5b1aeb`. The first build's hash `fa1c0e58…` is superseded; its cloud-gate record (`ci-run-41960481296/`) is kept as history.

The audit's mutant families are finite and written by the same author. Zero survivors means the gold now detects every requirement violation this audit can express; it does not prove exhaustive correctness.

## Amendment 1 (after the independent read-through review)

See `PROTOCOL.md` § Amendment 1 and `independent-review/case-review-008-009/DISPOSITION.md`. The rebuilt candidate:

- **Linux validation:** **72/72 suites, 1,557 cases; 483/483 designated mutants** rejected at their declared witness (`validation-001/summary.json`). The two new TR030 cases and shape-first mutant R10 account for the +2 and +1.
- **TR058 overlay:** rebuilt against the new hash. Its messages are unchanged (`f2484474…`), because TR058 is not affected by the amendment.
- **Audit rerun, 008 → 009:** 19 → **0** surviving confirmed mutants out of 973; **0 new** (`independent-review/c007-rubric-audit/results-008-vs-009/`, regenerated).
- **Cloud gates,** Actions run [41963290722](https://github.com/TronBronson1/qwenny-finetune-study/actions/runs/41963290722):
  - Windows Python 3.15.2 / pytest 9.2.0: **passed**. Hash `a3f14259…` verified; 72/72 suites, 1,557 cases, 483/483 mutants.
  - Pinned tokenizer: reproduces S007 exactly. Total **64,384** chat tokens. Only TR058 is over 2,048 (2,957); its overlay is **1,967**, and the maximum full training chat with the overlay is **2,021**.
  - `TRAINING_FIT_OVERLAY.json` was regenerated for the amended hash.
