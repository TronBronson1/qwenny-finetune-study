# S007 measurement repair results

Completed November 4, 2026. No optimizer updates or model generation occurred under S007.

## Validated repair

candidate-007 contains only 60 training and 12 development tasks. Parent candidate-006, approved exports, models, S006 scores and reserved final/regression tasks are preserved. All 72 correct reference sources are unchanged.

- All 72 revised gold suites pass the correct reference: 1,475 pytest cases.
- All 407 designated mutants are rejected through declared, relevant witnesses.
- All five negative controls are rejected: empty, pass-only, assert-true-only, skip-only and unrelated runtime crash.
- Builder checks include 10,037 valid-domain reference/oracle comparisons.
- The seven main external behavioral gaps and TR027's additional gap are covered by the revised targets and validated fixtures.
- Generator-level ordinary nested-type repairs cover 16 task fixtures; this now has task-specific executable evidence rather than extrapolation from TR027 alone.
- The advisory structural scan has no remaining type/ASCII absence flags; eight keyword false positives and three order-review notices are explained in STRUCTURAL_REVIEW.md.

There are 216 legacy mutants and 191 additional requirement fixtures: 72 exact-return-type, 41 type-before-value, 22 nested-return-type, 18 nonmutation, 16 ordinary nested-int rejection, eight external adversarial copies, five bounds-exception, five additional ASCII and four targeted order/shape fixtures. These are correlated finite checks, not 407 independent task families or a general coding-quality measure.

One proposed ASCII mutation for TR057 produced no relevant finite witness and was not promoted. No mutant was counted merely because a process exited nonzero.

## Scoring design

Instruction compliance, reference validity, behavioral coverage and mutant evidence are separate layers. All-or-nothing acceptance must not hide these graded measures.

Wrong exception classes can count only on declared contract-invalid witness inputs, where the reference's expected class and mutant's observed class are fixed and standard validation exceptions differ. There are 51 such declared witnesses. Crashes on valid return-value cases remain ineligible. This prospective fixture policy differs from S006's conservative rule; S006 has not been rescored.

The source predicate used for gold calibration is an advisory structural check; it is not a general semantic verifier for arbitrary model-written suites. Full-suite model evaluation still needs source/requirement review and witness binding.

## Hardware budget

The original revised training chats peak at 2,852 tokens; only TR058 exceeds the prior 2,048-token chat capacity. A first presentation preview reached 2,176 and was not accepted as a fit.

A second TR058 presentation preview reached 1,878 tokens by shortening task-specific mapping prose and removing display IDs/optional comma whitespace. Executable AST is identical except pytest display IDs. Its reference and all six designated mutants have identical per-case pass/fail/error/skip vectors to the calibrated gold: seven executions of 66 cases each. No case, assertion or behavior requirement was removed.

Using that explicit overlay, the profiled maximum across all 60 chats is 2,021 tokens. This is tokenizer evidence only, not a training export, loss-mask check or new actual longest-example backward. The overlay and its provenance are separate; candidate-007 itself remains unchanged. No output cap or GPU-fit claim was silently enlarged.

## Provenance and limitations

validation-001 failed on Windows worker directory creation; its logs/source remain as infrastructure evidence, excluded from calibration. validation-002 used main-process setup/logging and four bounded pytest subprocesses, taking about 202 seconds.

The first metadata-binding attempt found LF/CRLF differences between executed gold copies and source. Normalized UTF8 text and AST match exactly; references/mutants match bytes. No executable source was changed to fix a score.

Post-validation normalization corrected inherited oracle/count/status metadata and clarified the authoring README. Original and final source manifests, and the unchanged-code binding, are in calibration-certificate.json. The final candidate manifest hash is 3fb896ac4454be77d7ea98a777a50678e9ca4824d8dfe5572ad8aae4a6f438f5.

Review is finite and by the coordinating agent. External review of parent artifacts informed the repair; no independent acceptance of all revised tasks is claimed. Final/regression contents were not opened or imported. Broad target balancing and new training remain separate decisions.

## Evidence

- [Calibration certificate](calibration-certificate.json)
- [Definitive calibration execution](validation-002/summary.json)
- [Structural review](STRUCTURAL_REVIEW.md)
- [Original token profile](token-profile.json)
- [Fit-preview profile](length-preview-002/profile.json) and [runtime equivalence](length-preview-002/validation.json)
- [Candidate snapshot](../../dataset-v1/candidate-007/README.md)

Next: fixed-input component diagnostic S008, using existing weights only. It does not claim that repaired targets improved a model that has not been trained on them.

