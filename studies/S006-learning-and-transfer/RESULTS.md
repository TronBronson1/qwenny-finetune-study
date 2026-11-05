# S006 results — learning, transfer, and completion

November 4, 2026 (America/New_York). Exploratory local RTX3080 diagnostic; see [frozen protocol](PROTOCOL_FROZEN.md).

## Summary

| Split | Model | Attempted/planned | Complete | Reference-valid | Reference + all mutants | Strict accepted |
|---|---|---:|---:|---:|---:|---:|
| training | base | 4/4 | 4 | 2 | 2 | 0 |
| training | original-e1 | 4/4 | 4 | 3 | 2 | 0 |
| training | original-e5 | 4/4 | 4 | 1 | 0 | 0 |
| development | base | 4/4 | 4 | 1 | 0 | 0 |
| development | original-e1 | 4/4 | 4 | 0 | 0 | 0 |
| development | original-e5 | 4/4 | 4 | 1 | 1 | 0 |

Counts are out of four tasks per split/arm. Training tasks are familiar, not transfer evidence. All development targets previously contributed teacher-forced loss. Exact sampled tasks are in selection.json; no random-sample or population estimate is claimed.

## Every first attempt

| Task | Model | Tokens | Stop | Reference-valid | Eligible mutant kills | Strict |
|---|---|---:|---|---|---|---|
| TR024 | base | 1029 | eos | False | None | False |
| TR024 | original-e1 | 1166 | eos | False | None | False |
| TR024 | original-e5 | 626 | eos | False | None | False |
| DV008 | original-e1 | 816 | eos | False | None | False |
| DV008 | original-e5 | 679 | eos | True | 3 | False |
| DV008 | base | 991 | eos | True | 2 | False |
| TR025 | original-e5 | 1467 | eos | False | None | False |
| TR025 | base | 1238 | eos | False | None | False |
| TR025 | original-e1 | 991 | eos | True | 2 | False |
| DV004 | base | 1244 | eos | False | None | False |
| DV004 | original-e1 | 1831 | eos | False | None | False |
| DV004 | original-e5 | 1774 | eos | False | None | False |
| TR038 | original-e1 | 795 | eos | True | 3 | False |
| TR038 | original-e5 | 646 | eos | True | 2 | False |
| TR038 | base | 828 | eos | True | 3 | False |
| DV011 | original-e5 | 957 | eos | False | None | False |
| DV011 | base | 1532 | eos | False | None | False |
| DV011 | original-e1 | 1155 | eos | False | None | False |
| TR049 | base | 1352 | eos | True | 3 | False |
| TR049 | original-e1 | 850 | eos | True | 3 | False |
| TR049 | original-e5 | 1109 | eos | False | None | False |
| DV007 | original-e1 | 1894 | eos | False | None | False |
| DV007 | original-e5 | 641 | eos | False | None | False |
| DV007 | base | 1494 | eos | False | None | False |

## Source and rubric findings

- **TR024/base:** Wrong expected values for mixed ASCII/non-ASCII strings; conditional assert can assert a truthy string rather than compare; unsupported new-object identity requirement. Empty string and exact output str type missing. Source read completely; no unsafe operations observed.
- **TR024/original-e1:** Wrong AbCd expected value; rejects an actual str as invalid; calls valid-only function with dict/list without expected exception; contradictory and unsupported string identity assertions. Missing str-subclass rejection and exact output str test (isinstance insufficient). Full source read; no unsafe operations.
- **TR024/original-e5:** One wrong mixed-case expected result: Aa1! must become AA1!, not Aa1!. Exact output-type helper and input subclass tests present. Generic prose maps case IDs without a concrete requirement-specific map. Full source read; no unsafe operations.
- **DV008/original-e1:** Wrong distances include test->ttest expected2 rather than1, ABC->abc expected4 rather than3, and 123->321 expected3 rather than2. No str-subclass rejection at either position, no literal non-ASCII examples. Exact int return tested. Full source inspected; no unsafe operations.
- **DV008/original-e5:** Values appear correct and exact int return plus str-subclass rejection at both positions are present. Japanese-to-empty checks literal Unicode length, but no case-differing pair tests explicit case sensitivity, so frozen required coverage is incomplete. Full source inspected; no unsafe operations.
- **DV008/base:** Listed distance expectations appear correct; input str-subclasses at both positions and Unicode/case sensitivity are tested. No exact built-in int output assertion, so an int subclass could pass. Full source read; no unsafe operations.
- **TR025/original-e5:** Malformed nested/starred tuple construction with mismatched delimiters; ListChild built with multiple positional arguments; valid-case inputs incorrectly use subclasses; functions named run00000 are not pytest test functions. No proper valid-list behavior coverage. Full source read; no unsafe operations, syntax/collection failures retained.
- **TR025/base:** Valid run expected values appear correct, but nested list is invalid and is called without expected TypeError. No list-subclass rejection, no exact recursive output types, and valid mutation check compares only id (does not catch in-place changes). Full source read; no unsafe operations.
- **TR025/original-e1:** Run expectations and valid input nonmutation check appear correct. No input list/str-subclass rejection tests. Recursive output checks use isinstance and allow subclasses, contrary to exact-type requirement. Full source read; no unsafe operations.
- **DV004/base:** Valid [1,1] expected TypeError and valid [5,0] expected ValueError. Conditional identity assert becomes assert0 on empty input; identity comparison is not nonmutation. No actual list/int subclass tests, no exact int return, no mixed type/value ordering witness. Full source inspected; no unsafe operations.
- **DV004/original-e1:** Wrong XOR results: four5s should0 not5; 255^100^200 is83 not55. Float/str/None/MyInt256 incorrectly expect ValueError instead of TypeError. MyList nested as element does not test outer list-subclass rejection. isinstance int and not bool still allows int subclasses; exact output missing. Full source inspected; no unsafe operations.
- **DV004/original-e5:** Syntax-invalid parametrization (id assignment placed inside list and stray closing delimiters); unsupported explicit keyword; supposed valid case passes int not list; empty/valid byte lists incorrectly expect ValueError; invalid element types also assigned ValueError. Full source read; no unsafe operations, syntax failure retained.
- **TR038/original-e1:** Listed valid/invalid expectations appear correct and str-subclass rejection present. No exact output int assertion, no non-ASCII digit/lookalike rejection, and no malformed str-subclass precedence witness. Full source inspected; no unsafe operations.
- **TR038/original-e5:** Listed expectations appear correct, exact int output and malformed StrChild type-before-value witness present. Missing non-ASCII/fullwidth digit rejection and no mixed alphabetic-case example such as aB. Frozen ASCII/case coverage incomplete. Full source read; no unsafe operations.
- **TR038/base:** Listed hex and exception expectations appear correct. No exact built-in int output assertion, no non-ASCII/fullwidth digit rejection, no malformed StrChild precedence witness. Full source inspected; no unsafe operations.
- **DV011/original-e5:** Valid args are lists rather than single-element argument tuples, so interval_union(*args) passes wrong count/types; empty input unpacks empty list into no arguments. Several exception cases test wrong arity rather than contract validation. Recursive type helper never called. Missing input subclass/bool and ordering/shape witnesses. Full source read; no unsafe operations.
- **DV011/base:** Unsorted overlapping intervals [(3,7),(1,5)] incorrectly expected as two intervals instead of [(1,7)]. Missing empty case, mutation check, input subclass/bool and mixed-invalid ordering checks; output isinstance checks permit subclasses and omit exact outer list type. Full source read; no unsafe operations.
- **DV011/original-e1:** Unsorted case wrongly retains nested (1,2) instead of merging into (0,2). Invalid parametrization wraps each intended input with None, so all calls receive an invalid outer tuple and do not isolate advertised validation. Accepts TypeError or ValueError indiscriminately. Missing exact recursive output/input subclass/bool/mutation/precedence checks. Full source read; no unsafe operations.
- **TR049/base:** Listed results and exceptions appear correct; float/bool/str checks at all four positions. No int-subclass tests at any position, no exact output int assertion, no single-cell successful case. Some shape-before-bounds/type-value witnesses exist via zero dimensions. Main guard only runs when script invoked directly, not pytest import. Full source read; safe for isolated execution.
- **TR049/original-e1:** Listed values/exceptions appear correct on reference, but uses object identity is expected instead of value equality, an unsupported extra constraint (also implies built-in type at those cases). No ordinary invalid-type or int-subclass cases at four positions; no single-cell success. Main guard inactive under pytest. Full source read; safe for isolated execution.
- **TR049/original-e5:** Wrong offset: (1,1,2,2) expected4 instead of3. Nonpositive exact-int shapes incorrectly grouped under TypeError; out-of-bounds expects ValueError instead of IndexError; valid (0,1,1,2) and (1,1,2,2) incorrectly treated as errors. No non-square successful example. Exact output and input bool/subclass checks present. Full source read; no unsafe operations.
- **DV007/original-e1:** Many wrong neighbor lists/order: top-left expects down before right; one-column grid includes out-of-bounds column1; valid cells sometimes expected to raise; one intended valid row is outside shape. Broad exception tuple masks exception-class requirements. Missing int-subclass and exact coordinate types; right-order test is pass. These failures do not hinge on outer-container wording ambiguity. Full source read; no unsafe operations.
- **DV007/original-e5:** Single-cell grid wrongly expected to have neighbor(1,0); other lists omit neighbors/include out-of-bounds coordinates and violate order. Negative coordinates wrongly expect ValueError rather than IndexError; valid(1,1,2,2) expected IndexError. No exact recursive coordinate type checks; wrong-arity exception case. Failure independent of outer-container wording ambiguity. Full source read; no unsafe operations.
- **DV007/base:** Expected neighbor lists include original cell, out-of-bounds coordinates, duplicates and wrong order. Thin-grid examples also wrong. Catch-all exception/pass tests accept invalid bounds behavior. Missing ordinary invalid types/int subclasses and exact coordinate type assertions. Clear failures independent of outer-container wording ambiguity. Full source read; no unsafe operations.

## Runtime and limitations

Model verification/loading/generation elapsed: 3254.0 seconds. Generation cells: 3175.7 seconds; 27105 generated tokens. Torch peak allocated/reserved: 7.38/7.44 GiB. GPU sampled minimum free: 692.0 MiB. Windows per-process memory samples: 0; missing process samples cannot establish shared-memory spill. Scoring/pre-generation CPU fixture checks and report preparation are outside generation timing.

One seed and four purposively selected families per split cannot establish general aptitude or isolate a failure mechanism. Training and development task sets differ in content and difficulty. No final/regression tasks, new training, retries, repairs, cloud, conversion or LM Studio changes. Same-agent source review and fixture checks are not independent scientific validation.

## Evidence

- [Machine results](results.json) and [source reviews](source-reviews.json).
- [Generation records](../../training-v1/probes/s006-001/report.json).
- [Unchanged execution results](../../training-v1/scoring/s006-001/summary.json).
- [Preflight](preflight.json), [frozen hashes](freeze-manifest.json), [coverage rubric](COVERAGE_RUBRIC.json).
- Interpretation and next decision are recorded separately in INTERPRETATION.md after reviewing these results.
