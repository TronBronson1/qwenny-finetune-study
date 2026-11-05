# Pilot evaluator: operator material

This is a small development fixture, not the complete evaluation harness. On November 3, 2026, Python 3.12.10 checks verified nine valid reference cases, 18 invalid-type cases, and two exception/precedence cases (29 checks total). All six documented mutant witnesses were also confirmed against separate in-memory versions. No Qwen-generated suite has been evaluated yet.

Correct `clamp_value.py`:

```python
def clamp_integer(value, lower, upper):
    if any(type(item) is not int for item in (value, lower, upper)):
        raise TypeError("all arguments must be exact built-in integers")
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    return min(max(value, lower), upper)
```

Independent acceptance checks before using it as an oracle:

| Arguments | Expected |
| --- | --- |
| (5, 0, 10) | 5 |
| (-3, 0, 10) | 0 |
| (12, 0, 10) | 10 |
| (-5, -10, -1) | -5 |
| (-12, -10, -1) | -10 |
| (0, -10, -1) | -1 |
| (0, 0, 10), (10, 0, 10) | 0, 10 respectively |
| (99, 4, 4) | 4 |
| (5, 10, 0) | ValueError |
| ("bad", 10, 0) | TypeError |

For each of True, False, a custom int subclass instance, 1.5, "3", and None, substitute it into each position of (5, 0, 10); all 18 cases must raise TypeError.

## Required single-defect versions

Make a separate directory per version; each holds an independent `clamp_value.py` and the identical generated test file. Keep the reference unchanged. Each mutant retains all other reference lines.

| Mutant | Change | Witness that should fail |
| --- | --- | --- |
| M1 | Replace exact-type predicate with `not isinstance(item, int)` | Boolean or int subclass is wrongly accepted |
| M2 | Validate only `(value, lower)` | (5, 0, 10.0) wrongly returns a result |
| M3 | Replace `lower > upper` with `lower >= upper` | (99, 4, 4) wrongly raises ValueError |
| M4 | Return `max(value, lower)` | (12, 0, 10) wrongly returns 12 |
| M5 | Return `min(value, upper)` | (-3, 0, 10) wrongly returns -3 |
| M6 | Move the reversed-bounds check before the type check | ("bad", 10, 0) wrongly raises ValueError |

Verify witnesses independently before scoring. A suite passes this pilot only if it passes the reference, meaningfully detects all six mutants, and covers every prompt requirement. M1's kill alone does not establish checking every invalid type in every position.

## Execution workflow

Review generated code before executing it. Ordinary Python execution has the user's file permissions; a timeout or separate working directory does not provide isolation. For this small local pilot, execute only reviewed test code.

In each fixture directory, run the selected Python interpreter with `-m pytest -q test_candidate.py`. Use explicit file selection to avoid unrelated test collection. Record exit code, output, collected count, and elapsed time. A collection/import error is an invalid suite, not a mutant kill. Save actual relevant assertion traces for repair feedback.

Do not compare raw pytest test counts as an accuracy score: parametrization can inflate them. Score the contract and the fixed bugs. Save original answers, repaired answers, and evaluator changes separately.
