# Development pilot: write tests for clamp_integer

Paste the task below into a fresh Qwenny chat. Do not include operator notes or the evaluator's implementation/mutants. This visible pilot is development material, never a held-out evaluation task.

---

Write a complete pytest file for `from clamp_value import clamp_integer`.

Contract: `clamp_integer(value, lower, upper)` accepts only exact built-in integers in every argument. Reject booleans, integer subclasses, floats, strings, None, and other types with TypeError. Validate all types before comparing values. If lower > upper, raise ValueError. Otherwise return lower when value < lower, upper when value > upper, and value when it is within the inclusive bounds. Negative bounds are allowed. Equal bounds are valid.

Examples:
- clamp_integer(5, 0, 10) returns 5.
- clamp_integer(-3, 0, 10) returns 0.
- clamp_integer(12, 0, 10) returns 10.
- clamp_integer(4, 4, 4) returns 4.
- clamp_integer(5, "0", 10) raises TypeError.

Acceptance requirements:
1. Test normal and negative ranges, below/above limits, exact endpoints, equal bounds, and reversed bounds.
2. Test True, False, an int subclass instance, 1.5, "3", and None in EACH of the three positions. Hold the other two arguments valid. Prefer explicit (value, lower, upper, expected_exception) tuples to conditional argument construction.
3. Test type-validation precedence with ("bad", 10, 0): expect TypeError, not ValueError.
4. Import and exercise the function; do not implement, mock, or edit it. Do not inspect its source or files. No external access or dependencies beyond pytest.
5. Return one complete Python code block, then a short requirement-to-input mapping and limitations. Do not claim tests were executed unless you executed them. Do not claim exhaustive coverage.

---

## Operator checks

Save the answer and its exact request/settings under a new runs directory before extracting the test file. The first attempt is scored before providing feedback. Use `EVALUATOR.md` to check the answer; keep its contents out of Qwenny's request.
