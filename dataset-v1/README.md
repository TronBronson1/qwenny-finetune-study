# Qwenny dataset v1 — assembled, independent review pending

> **Latest repair — November 4, 2026:** [candidate-007](candidate-007/README.md) is a separate training/development-only calibration repair. All 72 gold reference suites and 407 designated mutants pass the [S007 calibration](../studies/S007-measurement-repair/RESULTS.md). It is not a training export and does not inherit old hash approval. A validated fit overlay is separate. candidate-006, historical approved exports and CURRENT_CANDIDATE.txt remain unchanged. Snapshot authoring fields and older status text below are historical; use the program current state for decisions.

> **Current navigation — November 4, 2026:** See [program current state](../program/CURRENT_STATE.md). The user-authorized corpus has been used for original and compact training; those runs are complete. Historical approval and “no training” statements below and inside immutable candidate snapshots describe earlier stages. They do not revoke recorded user authorization or establish independent review. All 12 development targets have teacher-forced loss exposure; final and regression model evaluation remain reserved.

2026-11-04: A separate [compact-target derivative](../training-v1/prepared-compact-001/README.md)
preserves all substantive training checks and unchanged development targets.
Its paired validation and local training trial are complete; see
[compact trial results](../training-v1/COMPACT_TRIAL_RESULTS.md). This corpus and
the original approved export were not edited.

Latest: the user authorized training after corpus review; that exact-hash
authorization is recorded in USER_TRAINING_AUTHORIZATION_2026-11-03.json. The first
three adapters have now been trained and import-verified. See
[training results](../training-v1/README.md). The bounded generation pilot did not
demonstrate a strict acceptance gain. Authoring-time snapshot review placeholders
below are retained as provenance, not a request to repeat already-given approval.

Update after assembly: user review sign-off is recorded in
[USER_REVIEW_2026-11-03.json](USER_REVIEW_2026-11-03.json). The local 2048-token
fit check passed with the frozen input embedding explicitly stored in CPU RAM;
see [fit results](../lora-feasibility/FIT_2048_RESULTS.md). Snapshot review
placeholders below describe the authoring state and do not negate the later user
statement. No per-file review actions beyond that statement are asserted.

Current candidate: **candidate-006**. Earlier candidate folders are retained assembly
drafts; use this one for review. No model has been trained on this corpus.

| Split | Tasks | Declared families |
|---|---:|---:|
| training | 60 | 56 |
| development | 12 | 11 |
| final | 24 | 24 |
| regression | 12 | 10 |

The 60 training tasks ask for pytest suites from precise function contracts.
Development and final tasks use the same task type. Regression includes four
implementation tasks, four repairs and four explanations. All content was
originally authored for this project; no external dataset or failed Qwen answer
was used. Previously exposed batches/prefix-removal families stay in training;
rotation/clock parsing stay in development.

Automated evidence for this exact candidate:

- 104 executable reference suites passed, with 1861 pytest cases.
- All 312 designated single-defect mutants failed at a recorded result/post-state assertion or required-exception witness.
- Four original regression bugs reproduced; these are separate from mutant scores.
- Four explanation snippets reproduced their expected values; rubric scoring still needs a person.
- 10,696 valid-input checks against separate oracle methods passed.
- No declared family ID crosses splits, and no exact normalized reference-source clone crosses splits.
- No evaluator answers occur as assistant messages in development/final/regression model packets.

These checks are all same-author/agent evidence. They do not establish independent
review, exhaustive correctness, semantic family independence or statistical power.
Some mutants are simple type/boundary/cardinality defects; detection is not a
general quality score. Broader behavior and equivalent/invalid-mutant judgments
remain review work. General pretrained contamination cannot be excluded.

## Review and evidence

- [Training review table](REVIEW_TRAINING.md)
- [Review guide](REVIEW_GUIDE.md)
- [All 108 task records](candidate-006/INDEX.md)
- [Automated validation](validation-007/summary.json)
- [Token profile](token-profile-006.json)
- [Mechanical split/source audit](audit-006.json)
- [Draft approvals file](candidate-006/approvals.template.json)

Each task contains its contract, target, source record, separate reference/oracle,
explicit cases and three mutant witnesses. Evaluator files are separate from model
messages. References/oracles/mutants and final answers must not enter trainer input.
Automated results are in the separate hash-bound validation report; authoring-time
placeholders inside the snapshot are not the current validation result.

## Local length and training boundary

All 60 complete training chats total **60,552 tokens** under the
explicit thinking-disabled profiling setting: minimum 781, median
953, 90th percentile 1235, maximum
**1954**. Nothing was truncated. Token lengths depend on the final
chat/reasoning policy; that policy is not approved by this profile.

The longest example exceeds the 768-token GPU benchmark. Before task training,
measure the complete maximum-length example (approximately 2048-token capacity)
on the local 3080 with the chosen loss/masking path. The earlier 15–30 minute
planning allowance is not a new full-dataset runtime measurement.

No app shutdown is required for CPU-only assembly. Recheck dedicated/shared GPU
memory before the next GPU trial; do not close Claude, Edge or other apps automatically.

## Approval/export boundary

The candidate is not frozen or approved for training. export_reviewed.py requires
a passed exact-content validation, an independent family/split audit and explicit
per-training-record approvals tied to reference/spec/target/answer hashes.
The empty approval template must not be bulk-approved from test counts.
Export also does not select reasoning policy or validate assistant-only loss masks;
those are separate pre-training checks.

Candidate hash-manifest SHA256: 9ebcef8e0ad4dcf498afc5fde3a2a1c34517458ca2639d705e8a0ad04e1c4d9f.
