# S006 interpretation and decision

November 4, 2026. Completed local run s006-001.

## Finding

All 24 first attempts terminated normally within the 2048-token cap, with one complete candidate block per answer. Strict acceptance was 0/4 for base, original E1 and original E5 in each split. Eight suites passed the correct reference; five met the unchanged evaluator's reference-plus-three-mutant rule. See RESULTS.md and results.json for every cell.

Familiar-training reference-valid counts: base 2/4, E1 3/4, E5 1/4.
Development reference-valid counts: base 1/4, E1 0/4, E5 1/4.
These are descriptive counts for fixed, purposively chosen tasks, not population estimates or checkpoint rankings.

## What this changes

- Lack of answer completion is not the sole explanation for failure on this sample: all answers finished.
- Clear case-construction, expectation and exception-class errors occur on familiar training tasks too. Failure cannot be explained solely as transfer to new specifications.
- Some suites are executable and correct on the reference, and five meet the designated-mutant rule, but explicit coverage gaps remain. Do not describe every failure as syntax failure or total inability.
- The original distinction between predicting supplied targets and constructing reliable free answers remains important. No fresh loss measurements were made here.
- No candidate selected. Extra epochs, larger caps, precision changes or deployment are not justified automatically by this diagnostic.

## Concrete examples

- E5/TR024 expects Aa1! to remain Aa1! instead of AA1!.
- E5/TR049 expects offset 4 for (row 1, column 1, rows 2, columns 2), where the correct offset is 3; it also mixes exception classes.
- E1/TR025 passes the reference but does not test list/str subclasses and uses isinstance for exact recursive outputs.
- E5/DV008 passes the reference and meets all three designated mutant checks but lacks a case-differing string pair required to test case sensitivity.

## Measurement limits requiring review

The sample spans target lengths, not a random task distribution; training and development tasks have different content/difficulty. All development targets had prior teacher-forced loss exposure. E1/E5 are checkpoints on one trajectory, not independent runs. One seed cannot establish robustness. No strong-prompt demonstration arm was included, so the original practical adoption comparison was not performed.

Source/coverage review was by the coordinating agent. Gold checks and hashes do not establish independent semantic correctness. DV007's outer-container wording is less explicit than the authored target; all three DV007 candidates also have clear coordinate/order/exception errors independent of that ambiguity. No verdict hinges only on the ambiguous outer-container preference.

The unchanged scorer credits AssertionError / DID NOT RAISE witnesses, not arbitrary nonzero exits. In DV008/base/M03 the mutant crashes with IndexError, so this is not credited. In TR038/E5/M01 malformed StrChild('x') produces unexpected ValueError instead of required TypeError; this is excluded by the scorer's conservative rule. Whether such related wrong-exception failures should receive semantic credit deserves a prospective evaluator-policy review. Preserve current machine counts and logs; do not silently reclassify them as either ordinary assertion kills or mutant survival. Strict acceptance remains false for these candidates on other explicit coverage grounds.

No new model attempts, extra mutants, repairs or alternative scores were introduced after the results.

## Recommended next work

Prioritize a CPU-only task/prompt/evaluator audit before another GPU training run:
1. Review these eight specifications, supplied targets and designated defects with a separate reviewer, restricted to training/development material.
2. Resolve hidden target preferences, precise exception policy and what constitutes meaningful requirement coverage.
3. Audit whether general system instructions introduce irrelevant requirements (e.g. reversed bounds on a string parser) and whether target presentation reliably models correct argument construction.
4. Produce a versioned audit and one bounded follow-up proposal. Keep original S006 scores and data unchanged.

If that review supports proceeding, design one narrow intervention aimed at case construction or training/inference alignment, with a matched base control. Do not choose its settings by opening final/regression tasks. No additional training was performed or started here.

