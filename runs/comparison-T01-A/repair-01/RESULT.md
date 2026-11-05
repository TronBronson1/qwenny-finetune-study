# T01-A: after one repair

Source: user-supplied pasted attachment, preserved verbatim in `response.md`; Python block extracted into `test_candidate.py`. Intended repair request copied into `intended_request.txt`; exact submitted request and effective settings remain user-operated and not independently verified. Generation time, tokens and stop reason not supplied.

Executed unchanged with Python 3.15.0 / pytest 9.2.0 against the same frozen T01 fixtures.

Reference result: **32 passed, 3 failed**. Acceptance: **FAILED**. Reference-invalid suite; mutant detection score is ineligible. All five mutants also exit 1, but their failures receive no detection credit because the suite rejects the correct implementation. Full logs and exit codes retained in `evaluation/`.

The three reference failures:

- `((1, 2), -1)` incorrectly expects `(1, 2)`; the contract requires `(2, 1)`.
- `((1,), (2,), (3,))` is a valid exact built-in tuple, not a tuple-subclass instance; expecting TypeError is incorrect.
- `({1: "a"}, {2: "b"})` is also a valid exact built-in tuple, and arbitrary elements including dicts are allowed; expecting TypeError is incorrect.

Remaining category gaps: positive and oversized rotations generally assert only the return type, not the expected order. Duplicate cases assert type/length but not element preservation or order. Nested cases assert only tuple type; comments do not establish element identity or absence of mutation. No actual tuple or integer subclass is constructed, and no invalid steps are exercised with empty values. Exact built-in result type is not established by isinstance alone, though the contract requests a tuple and does not explicitly prohibit tuple-subclass results.

Prose accuracy: no affirmative execution claim. Mapping overstates direction, wrap, identity and mutation coverage; it also names step cases that are in other tests. Several stated limitations are false: int/tuple subclasses can be defined locally; expected rotation order can be checked directly from the contract; nested content can be compared with saved expected content without modifying originals. Exact exception messages are outside the contract. Three sampled empty steps do not cover all step combinations.

First-attempt and one-repair outcomes are both failed. No second repair is permitted in the scored comparison. Next: fresh chat with `prompt-comparison/packets/T01-B.txt`, current system prompt/settings and matching seed 42. B contains both fixed demonstrations and the unchanged task; do not include A's response, repair or evaluation feedback.
