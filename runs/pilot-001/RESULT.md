# Pilot 001 — first attempt rejected

November 3, 2026. User-supplied Qwenny response saved as `test_candidate.py`. Context setting confirmed by user: 16134. Intended settings: LM Studio baseline in `../../04_LM_STUDIO_BASELINE.md`, thinking on and seed 42; exact sent prompt, model file hash, generation timing and full response metadata not independently captured. The user supplied a Python block only; any omitted prose cannot be assessed.

## Executed evidence

Evaluator: Python 3.15.0 environment (pythoncore-3.15-64), pytest 9.2.0. Python 3.12.10 was available but lacked pytest, so no packages were installed. Exact Python patch version should be captured separately if needed.

The submitted suite ran unchanged against the reference and each of six separate mutants. All seven runs exited 2 during collection with `ModuleNotFoundError: No module named 'my_module'`. The contract requested `from clamp_value import clamp_integer`. Individual logs are in each fixture's `pytest.log`.

Reference validity: failed. Valid mutant detection score: not applicable. Collection failures do not count as kills. No task-level tests executed successfully in the scored attempt.

A separate diagnostic copy changed only the import, leaving the original untouched. It also exited 2 during collection:

    In test_candidate.py::TestClampInteger::test_type_validation_precedence: function uses no argument 'bad_input'

This diagnostic is not a repaired model answer or a second scored attempt.

## Additional issues found by inspection

- Two test methods request a `clamp_integer` fixture, but no fixture is supplied. An imported function is not automatically a pytest fixture.
- `pytest.raises(ValueError)` returns a context manager, not a class. Therefore `isinstance(expected, type)` does not select the intended exception branch. The reversed-bounds case would raise an uncaught ValueError after earlier blockers are removed.
- The parametrized precedence method has a `pass` body and cannot establish any requirement. One comment also incorrectly labels a tuple/string input as a Boolean lower-bound case.
- The 18 invalid-type cases use clear argument positions and specific expected exceptions; these are useful elements to preserve.

## Next step

Update: the user's one-repair response has now been evaluated. See `repair-01/RESULT.md`: 29 passed, 1 failed against the correct reference; after-one-repair acceptance failed. Any further revision is additional development beyond this scored attempt.

One compact repair request using actual failures and the unchanged contract. Preserve all original files/logs. Do not supply a complete corrected answer to the model. Score the corrected suite against the unchanged reference and all mutants; keep first-attempt rejection separate from repair success.
