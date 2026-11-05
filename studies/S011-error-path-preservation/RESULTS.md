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
| TR058 fit overlay rebuilt for 009 | AST equal ignoring display ids; per-case results identical for reference + 9 variants; token count pending CI |
| Windows Python 3.15 validation and pinned-tokenizer profile | pending: `.github/workflows/s011-cloud-gates.yml` |

Candidate hash (`SHA256.json`): `fa1c0e581a1076775cfcc9e775b18f2805dd7459cf5d7f9dadeaa6ba44dfff64`.

The audit's mutant families are finite and written by the same author. Zero survivors means the gold now detects every requirement violation this audit can express; it does not prove exhaustive correctness.
