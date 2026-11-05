# Qwenny handoff: dataset v1 assembled, independent review pending

Date: 2026-11-03, America/New_York.

User chose to stay on the local RTX 3080. Do not switch to cloud or incur costs.
User operates LM Studio; Codex manages experiment files/evaluation. Preserve models,
past prompting results, trial logs and dataset snapshots. Project sources/ is read-only.
Do not close apps automatically. The user offered to pause Claude/close apps if
needed; CPU assembly did not require that and no apps were terminated.

## Current dataset

Directory: C:\Users\jalar\Desktop\Chat AI Lab\AI Labwork\Qwen\Fine Tuning Test\dataset-v1.

Current review candidate: **candidate-006**. Earlier candidates are retained drafts.
Read README.md, REVIEW_TRAINING.md and REVIEW_GUIDE.md first.

- 60 training tasks, 56 declared families.
- 12 development tasks, 11 families.
- 24 final tasks, 24 families.
- 12 regression tasks, 10 families: four implementations, four repairs, four explanations.
- 108 records / 101 declared families; no declared family ID crosses splits.
- Existing batches/prefix-removal families remain training candidates.
- Previously visible rotation/clock parsing remain development, never unseen final tests.
- No raw/failed Qwen output or external dataset copied.

Task folders contain contracts, complete target answers, explicit pytest cases,
separate references/oracles, three concrete single-defect mutants and review records.
Model-packet JSONL outside training contains requests only. Evaluator answers,
references, oracle code and mutants must stay outside trainer input.

All targets remain pending independent review. Automated same-author checks are
not human review. The user's review of earlier feasibility details did not approve
these new records. training-candidates.jsonl is not approved trainer input.

## Validation and integrity

Current automated report: validation-007/summary.json.
Python 3.15.0, pytest 9.2.0:

- 104 reference suites / 1861 pytest cases passed.
- All 312 designated mutants detected at a relevant result/post-state assertion or
  required-exception witness; crashes/timeouts alone do not count.
- Four original regression bugs reproduced separately.
- Four explanation evidence snippets reproduced expected results; human rubric scoring pending.
- 10696 valid-input checks against separate oracle calculations passed.
- audit-006.json: no exact normalized source clone crosses splits; no held-out
  assistant answers in model packets. Semantic family audit is still required.
- Validation reused 139 completed identical source/target executions; changed
  targets were executed again. Earlier Windows stdout-encoding issues were fixed,
  and logs retained. Unused drafts are not the current dataset.

Current SHA256.json fingerprint:
9ebcef8e0ad4dcf498afc5fde3a2a1c34517458ca2639d705e8a0ad04e1c4d9f.

export_reviewed.py requires a passed exact-content validation, an independent
family audit and all 60 training approvals with reviewer notes and exact source,
spec, target and answer hashes. The rejection path was checked: the unapproved
template cannot create trainer input. See export-guard-current-check.json.

## Length, runtime and next steps

token-profile-006.json: complete training chats total 60552 tokens; min 781,
median 953, p90 1235, max 1954. No truncation. Profiling used an explicit
thinking-disabled template setting only for sizing, not an approved training policy.
Targets are direct pytest answers plus mapping/limitations, without fabricated
private reasoning traces. Historical inference controls remain thinking-enabled.

The successful local ten-update chunked-loss benchmark covered 768 tokens,
approximately two seconds/update, with 82 MiB sampled process shared usage.
Standard 768-token loss exhausted dedicated memory; user observed about 1 GB
shared-memory overage. See lora-feasibility/REAL_LENGTH_RESULTS.md.
The full dataset now needs a roughly 2048-token capacity check with complete
targets and validated assistant-only masking. Do not truncate pytest answers to fit.
The prior 15–30 minute training allowance remains provisional.

Next: independent target and family/split review; pin reasoning/formatting policy;
measure max-length local fit and assistant-mask correctness; freeze hashes and
approved export; repeat matched base A/B controls in the chosen runtime before a
meaningful adapter comparison. Formal held-out scoring needs reviewed references,
fixed mutants/category rubric and no final-test feedback used for selection.

No task-training run has started. All adapters so far are disposable synthetic
feasibility artifacts. LM Studio export/merge/GGUF compatibility remains untested.
