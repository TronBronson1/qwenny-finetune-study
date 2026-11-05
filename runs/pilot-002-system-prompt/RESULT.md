# Pilot 002: reusable system prompt intervention

November 3, 2026. User reports earlier pilot system prompt was blank and this answer used the system prompt prepared in `../../05_FIRST_ALTERATION.md`. Raw submitted answer preserved in response.md; extracted test file preserved unchanged. This is a prompt/context alteration, not a weight update.

The precise full request, fresh-chat status, effective runtime metadata, timing, and any additional conversation turns were not supplied. Baseline settings remain intended settings, not independently captured request evidence. This is a reused development task; no causal improvement or unseen-task generalization can be inferred from this single comparison.

Executed with Python 3.15.0 and pytest 9.2.0 against the unchanged fixtures from pilot 001:

| Implementation | Actual result |
| --- | --- |
| Reference | 23 passed, 3 failed |
| M1 | 17 passed, 9 failed |
| M2 | 20 passed, 6 failed |
| M3 | 22 passed, 4 failed |
| M4 | 21 passed, 5 failed |
| M5 | 22 passed, 4 failed |
| M6 | 22 passed, 4 failed |

Acceptance: FAILED. Valid mutant score is ineligible because the suite fails the correct reference. See each implementation directory's pytest.log and execution_summary.json.

Follow-up: the one-repair answer is accepted, with 28/28 reference tests passing and meaningful detection of all six mutants. See `repair-01/RESULT.md`. This does not change the first-attempt failure recorded above.

All three reference failures are `NameError: name 'MyInt' is not defined`. MyInt is defined inside TestClampIntegerIntSubclassInvalid but referenced by bare name inside method lambdas. A class attribute is not an enclosing lexical binding for those method bodies. The target function is never called in these three failed cases. A simple repair is defining MyInt at module level, or explicitly using self.MyInt in each method.

The reversed-bounds case now works and the earlier mixed return/exception branching is absent. The callable form `pytest.raises(TypeError, lambda: ...)` itself is valid; it is not the source of these failures.

Coverage issue: the mapping describes equal bounds `(4,4,4)` as exact endpoints, but there are no separate lower/upper endpoint tests with distinct bounds, such as `(0,0,10)` and `(10,0,10)`. Those were explicitly requested by the original pilot. Passing the fixed mutants would not alone establish full requirement coverage.

Reporting: the answer correctly says tests were not executed and avoids an exhaustive-coverage claim. Its subclass coverage claim describes intended tests, not successful validation. Test counts are not comparable accuracy percentages across versions.

Next repair, if pursued: supply actual NameError evidence, request module-level subclass definition and explicit distinct-bound endpoints, preserve all other tests, and rerun all fixtures. Do not treat this rejected answer as an approved training target.
