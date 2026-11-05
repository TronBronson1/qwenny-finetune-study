# Independent review 001 — disposition and correction

Received November 4, 2026, supplied by the user. [Original text](INDEPENDENT_REVIEW_001.txt) is preserved verbatim; SHA256: 70ef9b3b856af7678b0c9e6e62cbf7238b126f47c6699979b91598e19ed27c2c. Reviewer identity/tool and independence were not independently authenticated; provenance is user-supplied external review. Do not describe this response as a second independent review.

## Verified critical finding

Direct inspection of candidate-006 test_target.py and the frozen S006 rubric confirms:
- TR038 gold lacks non-ASCII/fullwidth digit rejection.
- DV008 gold lacks a case-differing string pair.
- DV011 gold lacks non-bool integer-subclass endpoint tests.

The gold suites passed reference/mutant execution preflight, but that did not establish that they satisfied the human coverage rubric. The coordinating agent omitted a gold-versus-rubric gate. The instruction requiring concrete coverage was stricter than the supplied examples in these respects.

S006's strict zero is the recorded outcome of its frozen rubric, not a validated stand-alone measure of model capability or training benefit. Do not use it for checkpoint adoption or a broad no-improvement claim. E5/DV008 in particular met the executable reference-plus-mutants rule and was rejected on a coverage item absent from its gold target too.

This does not erase observed wrong values, invalid syntax, wrong argument packaging or reference failures. The 24 completions, eight reference-valid suites and five suites meeting the conservative three-mutant rule remain descriptive results under the existing fixtures. Those fixtures and credit rules also require review; none are comprehensive quality measures.

## Accepted directions

Require rubric/contract/target alignment before another model study. Make test-design expectations explicit or report them separately from instruction following. Audit boilerplate relevance, declared return types, target balance and mappings. Add graded secondary measures alongside any all-or-nothing metric.

Develop requirement-linked mutants with executable witnesses, equivalence/validity review and gold checks. Do not equate one mutant per rubric item with exhaustive coverage. Where gold misses an explicit contract behavior, improve the gold prospectively; do not automatically weaken the requirement to fit the answer.

Review transfer at the semantic level. Shared grid signatures and validation structures make DV007 limited evidence of distant transfer even if declared family labels differ.

Keep revisions in new versioned artifacts. Preserve S006, candidate-006, approved exports and all trained models. Do not silently migrate old authorization to a changed corpus.

## Qualifications

The supplied review's broader 72-task inventory, proportions and duplication counts have not been independently re-counted in this response. The proposed audit must verify them.

M01 weakens exact-type checks generally, including strings and containers; it is not literally an int-only mutation on every task.

A pass-only test is vacuous but does not invalidate every other meaningful test in its suite. The scorer needs substantive-call/assertion checks and skip/xfail/collection review; test count alone is insufficient. Preserve the distinction between a weak suite and a suite containing one empty test.

Execution-claim detection needs semantic review. “Should pass” is a prediction, and “verified” may mean inspection; neither automatically proves a fabricated execution claim.

The wrong-exception policy must distinguish a relevant contract violation from an unrelated mutant crash. S006's narrow implementation and broader wording were not sufficiently aligned. Preserve its conservative counts; any alternative credit rule is a separately labeled, post-hoc analysis.

A three-task difference on 24 tasks is not automatically significant or automatically inconclusive in every design. Freeze paired task-level analysis, seed aggregation and uncertainty reporting before final evaluation. A practical threshold alone does not establish reliable benefit.

Thinking-disabled answers can still contain short calculation comments and correctly computed outputs. These results do not demonstrate that hidden reasoning or longer output would solve the problem. A fixed-input output-only diagnostic is a reasonable separate proposal, not an established remedy.

## Next gate

1. CPU-only alignment audit of the eight S006 tasks; then extend to all 60 training and 12 development tasks with task-appropriate rubrics. Do not imply all 72 already have frozen per-task rubrics.
2. Record each requirement's prompt wording, gold witness, mutant witness, ambiguity and disposition.
3. Declare a protocol before any exploratory case-level rescoring. Separate wrong expectations, valid/invalid argument construction, wrong exceptions, collection failures and unextractable cases; report denominators and extraction limits. Do not repair output or select only easy-to-extract cases without reporting exclusions.
4. Prepare a revised candidate only after audit decisions. Validate before new training or GPU generation. Final/regression contents remain reserved.

No new model execution, training, revised targets, mutants or rescoring occurred while incorporating this review.

