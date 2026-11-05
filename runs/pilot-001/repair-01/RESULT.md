# Pilot 001: one-repair outcome

November 3, 2026. Submitted repair preserved in `test_candidate.py`; executed unchanged with Python 3.15.0 and pytest 9.2.0 against the same seven fixture implementations. Logs and machine-readable summaries are saved beside this report.

| Implementation | Actual result |
| --- | --- |
| Correct reference | 29 passed, 1 failed |
| M1 | 19 passed, 11 failed |
| M2 | 25 passed, 5 failed |
| M3 | 28 passed, 2 failed |
| M4 | 27 passed, 3 failed |
| M5 | 27 passed, 3 failed |
| M6 | 28 passed, 2 failed |

After-one-repair acceptance: FAILED. Mutant scoring remains ineligible because the suite fails the correct reference. The additional mutant failures are diagnostic only; reporting these results as a valid 6/6 score would be misleading.

The repair fixed the wrong import, undefined fixture arguments, and mismatched parametrization/placeholder. The remaining failure is `test_valid_inputs_behavior[input_args9-expected9]` with arguments `(5, 10, 0)`.

`pytest.raises(ValueError)` is a context-manager object, not a class. `isinstance(expected, type)` evaluates false, so execution enters the ordinary-result branch and the reference's correct ValueError escapes uncaught. The model retained the exact pattern it was asked to examine.

The statement "Uses pytest.raises to handle exception-based assertions correctly" is not supported for that case. The Boolean-lower method also has a misleading name: `(5, True, 10)` has ordered bounds and checks type rejection, not precedence over reversed bounds. The separate string/reversed-bounds test does check the required precedence.

Interpretation: code improved from failing collection to 29 passing cases, but the single allowed repair did not meet acceptance. Keep this as a failure-and-feedback development record, not an approved training target. Any further repair is additional development beyond the prespecified one-repair score.

Minimal teaching correction: remove the reversed-bounds row from the normal-return table and put that case in its own test with `with pytest.raises(ValueError): clamp_integer(5, 10, 0)`. This suggestion has not been applied to the submitted answer or counted as a model success.
