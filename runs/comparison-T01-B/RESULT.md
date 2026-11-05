# T01-B: first attempt

Arm B: same task with both fixed demonstrations. User returned the answer after being directed to the T01-B packet in a fresh chat with unchanged settings and matching seed 42. Exact submitted request, fresh-chat state and effective settings were not independently verified. Timing, token count and stop reason not supplied.

First-attempt acceptance: **FAILED**. Executed unchanged with Python 3.15.0 / pytest 9.2.0. The limitations paragraph is plain prose inside the Python block, producing SyntaxError at line 106. No test bodies ran. All six fixture runs exited 2 with collection errors. Reference validity failed; mutant detection is ineligible, and no failures count as bug detection.

Static review identifies additional issues, not additional executed failures:

- `TupleChild(0)` cannot be constructed from a noniterable and would interrupt collection after parsing is fixed.
- `((TupleChild((1, 2)), 3), None)` has an ordinary outer tuple and invalid steps. It does not isolate a tuple-subclass values argument.
- Tuples containing booleans are valid under the arbitrary-element contract; the two such expected-TypeError cases are incorrect.
- For `(1, 2, 3, 4, 5)`, steps 6 should give `(5, 1, 2, 3, 4)` and steps 7 should give `(4, 5, 1, 2, 3)`. The supplied -7 expectation is correct.
- Nested equality cases establish neither object identity nor absence of mutation. Explicit assertions are missing.
- A conditional case violates the explicit-tuple instruction. Its `if False` branch does not evaluate undefined a/b, so these names are not an executed NameError.
- Requirement-to-input mapping is absent. The limitations paragraph copies an external-check-record reference from the demonstrations without identifying a record for this answer. No affirmative execution claim was made.

Some structure improved: locally defined int/tuple subclasses, separate return and exception tests, and many explicit expected results. These observations do not establish an accuracy improvement: both A and B first attempts failed, and only one task pair is available.

Preserved answer and code: `first/`. Full execution logs: `first/evaluation/`. Intended request snapshot: `first/intended_request.txt`. Single repair feedback: `REPAIR_PROMPT.txt`, with unchanged contract, actual failure output and static category review; no hidden evaluator code or mutant source disclosed.

After-one-repair outcome: **FAILED**. See `repair-01/RESULT.md`: the syntax error remains and collection fails. Both T01 arms are complete with failed first-attempt and one-repair acceptance. One task pair cannot establish broad demonstration effectiveness.
