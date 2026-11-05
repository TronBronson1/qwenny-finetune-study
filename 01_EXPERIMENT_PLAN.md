# Experiment protocol v0.1

## Hypothesis and comparison

An adapter trained on reviewed specification-to-test examples will increase first-attempt task acceptance on new task families compared with the same base model using a strong prompt plus two examples.

| Arm | Weights | Prompt |
| --- | --- | --- |
| A | Unchanged base | Shared task instructions, no demonstrations |
| B | Same base | Same instructions plus two fixed training-set demonstrations |
| C | Same base plus adapter | Same instructions as A |
| D, optional | Same base plus adapter | Same instructions and demonstrations as B |

A is an instructed baseline, not an unprompted model. B versus A measures examples; C versus A measures adaptation without examples. Compare C against B to answer the practical question. D tests whether effects combine.

Use one inference stack, base revision, tokenizer, chat template, numerical precision, and generation settings across A/B/C for the primary comparison. Ollama A/B results are useful operational baselines, but cannot by themselves isolate an adapter effect measured in a different training runtime. Repeat A/B in the eventual adapter runtime before comparing C. If exporting back to Ollama, compare exported base and adapted models at the same quantization separately.

## Task and scoring

Each task supplies a clear specification and function import name. The evaluator retains an independently checked correct implementation and a fixed set of single-defect implementations (mutants). Keep mutants and evaluator answers out of the model request. No third-party packages beyond pytest; no external services required by test code.

First-attempt task acceptance requires all of:

- A complete, collectable suite that imports the requested function without replacing or mocking it.
- All generated tests pass against the correct implementation.
- Every predesignated required mutant fails through a relevant assertion or expected-exception check. Import errors, crashes, timeouts, and deliberate inspection of implementation filenames do not count as bug detection.
- Every required specification category has a meaningful assertion. Review concrete inputs; test names alone do not establish coverage.

Also record reference pass rate, valid mutant kills/eligible mutants, missing categories, completion/truncation, elapsed generation time, and tokens when available. Compute mutant detection only for reference-valid suites; report reference-invalid suites separately rather than rewarding their failures. Review and exclude equivalent or invalid mutants before freezing the benchmark.

Score prose separately: claimed execution without evidence; unsupported completeness or coverage claims; acknowledgment of untested cases. An honest explanation cannot compensate for broken code, and passing code cannot validate an exhaustive-coverage claim.

## Fixed initial conditions

Active development pilot settings are recorded in `04_LM_STUDIO_BASELINE.md`: LM Studio 0.4.28, thinking on, temperature 1, top_p 0.95, top_k 20, presence_penalty 1.5, seed 42, approximately 16K context, no explicit response or reasoning cap. The loading screenshot shows 16134 while the loaded counter shows 16384; confirm the effective value before formal evaluation. This supersedes the original provisional settings. Later repeat with seeds 17/42/73 in fresh conversations for every task/arm/seed. Pin settings after development and before held-out evaluation. Save full messages and effective settings, not only the intended values. Check prompt plus output fits the context, especially for arm B.

Use one sample per task/arm/seed; never select the best of several attempts. Three seeds measure variability; they do not create three independent tasks. Aggregate per task and report task counts and paired arm differences. Rotate arm order across tasks. Track warm/cold model loading separately from generation time. Record token-limit stops as incomplete, even if the prose sounds finished.

## Repair is a separate experiment

After scoring the first attempt, allow at most one repair with the actual failure output, the unchanged specification, and the instruction: "Correct only the failing tests. Return the complete corrected file. Trace the concrete argument pair for each changed case. Do not claim execution."

Apply the same feedback policy to every arm. Report first-attempt and after-one-repair acceptance separately, along with time and handling effort. Avoid leaking hidden test failures into training or prompt tuning after final evaluation begins.

## Dataset and regression budget

Initial collection target: 60 training tasks, 12 development tasks, 24 held-out tasks, and 12 separate regression tasks. These are planning targets, not a claim of sufficient training data or statistical power. Prefer more independently reviewed task families over many rewordings. The discount example and this folder's pilot are development material and excluded from held-out scoring.

Regression tasks cover small Python implementation, bug repair, and explaining a concrete failure without inventing execution. Use executable acceptance checks for code and a fixed human rubric for explanations. Keep these outside adapter training.

## Decision rule, frozen before final test

Provisional adoption threshold: C improves task acceptance over B by at least 10 percentage points on held-out tasks, adds no more than one failed regression task compared with B, and shows no increase in fabricated execution claims. Report paired wins/losses and uncertainty; a small sample may remain inconclusive even if it crosses this practical threshold. Do not claim general coding improvement from this narrow benchmark.

Use development results for prompt selection, training choices, and checkpoint selection. Evaluate the frozen final test once per selected arm/seed. If test results guide revisions, retire that test set from final use and assemble a new one.

## Milestones

1. Verified environment and written protocol: established November 3.
2. Development pilot and evaluator checks: pending.
3. Reviewed split dataset and A/B baseline: pending.
4. Compatible training stack, load/backward/save/reload memory trial: pending.
5. Small adapter run, development selection, final paired evaluation: pending.
