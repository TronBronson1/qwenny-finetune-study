# S007 — CPU-only measurement repair

Declared November 4, 2026, before new candidate validation. User authorized improvements and continued testing/documentation after adversarial review.

## Scope

Prepare candidate-007 as a training/development-only derivative of candidate-006: 60 training and 12 development tasks. Do not import final/regression task definitions or open reserved task content. Preserve all original data, approved exports, models, S006 outputs and scores. No optimizer updates or model generation in S007.

## Repairs

- Fix ordinary wrong-type and endpoint-subclass coverage at the generator/schema level.
- Add the demonstrated ASCII-digit, case-sensitivity and ordinary-element behavioral witnesses; review remaining flagged tasks semantically, not by keywords alone.
- Add task-specific boundary/order examples where reading the contracts and existing cases reveals gaps. Validate new expected values with the separate original oracle and reference, without using failed model outputs as targets.
- State return structures explicitly, condition nonmutation instructions on applicable inputs, remove irrelevant reversed-bounds boilerplate, and expose coverage expectations in model-facing instructions.
- Preserve substantive old examples; remove unused output-helper branches and replace generic mapping prose with task-specific case/category mappings. Defer wholesale case rebalancing, calculation-comment training and optimizer changes to separate studies.
- Add requirement-linked proposed mutants, including the eight external witnesses, nested-type validation and selected semantic checks. A mutant is promoted only if a concrete contract violation is witnessed and the revised gold detects it; document unrelated-crash and equivalent/surviving candidates instead of counting them as kills.

## Calibration gate and metrics

All revised gold suites must pass the unchanged correct reference with nonempty meaningful tests and no skips/xfails. All designated valid mutants must be rejected through the declared witness: wrong returned value, mutation of valid input, omitted required exception, or a declared wrong exception class on a contract-invalid input. Unexpected crashes on valid-input value tests receive no credit.

Maintain per-task traceability from explicit contract/prompt requirements to gold cases and mutant/review evidence. Structural scans are advisory. Record finite same-agent semantic review separately from the external eight-task review; neither implies exhaustive correctness.

Report reference validity, instruction compliance, behavior coverage and mutant outcomes separately. Any overall acceptance rule is additional to these graded measures. Empty/pass-only tests contribute no substantive coverage; the presence of one empty test does not invalidate other meaningful tests. Execution-claim flags require semantic review and must distinguish predictions from claimed execution.

## Validation and limits

Run selected negative-control calibration and all 72 revised gold suites against reference and designated mutants using established Python3.15/pytest9.2, isolated work directories, disabled plugin autoload and bounded subprocess timeouts. Keep raw logs and exact sources. Retain original three mutants with provenance and add validated requirement mutants under new IDs; do not rewrite S006's denominator.

Profile revised training chat lengths with the pinned tokenizer, CPU only. No silent sequence/token-budget increase or changed-corpus export approval. Do not start training if lengths or measurement alignment remain unresolved.

A fixed-input expected-output-only model diagnostic may follow under its own frozen protocol after calibration. Rescoring S006, if later justified, is a separately declared post-hoc sensitivity analysis, never a retrospective first success.
