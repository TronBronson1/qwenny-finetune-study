# T02-A: first attempt

Arm A: instructions without demonstrations. User returned the answer after the fresh T02-A chat request. Intended packet saved; exact submitted input, fresh-chat state and effective settings not independently confirmed. Seed 42 and unchanged settings requested. Timing, token count and stop reason not supplied.

Executed unchanged with Python 3.15.0 / pytest 9.2.0: **15 reference tests passed; 5/5 fixed mutants detected**. Relevant failures: arithmetic (12:30, 23:59), hour boundary (24:00), minute boundary (12:60), str-subclass acceptance (_FakeStr), and Unicode-digit acceptance (fullwidth digits). Reference-valid and mutant detection eligible. Full logs retained in `first/evaluation/`.

Strict first-attempt acceptance: **FAILED: missing exact-result-type assertion**, the same missing category as T02-B's first attempt. Equality with expected integers permits equal-valued floats and int subclasses. The original contract requires an exact built-in int. The frozen mutant set does not cover that distinction, so 5/5 detections do not establish full acceptance.

Required sampled categories otherwise present: midnight, interior time, end of day, hour/minute bounds, malformed field widths, whitespace, Unicode digits and invalid types including an actual str subclass. No same-length wrong-colon or ASCII nondigit case and no direct sign example; these limitations do not expand the frozen scoring requirements or mutant set. Boolean input types are not explicitly sampled; not every invalid type is required to be enumerated.

Prose: no fabricated execution claim. Mapping is generic rather than tied to concrete cases. The limitation suggesting coverage can be inferred from standard validation patterns is unsupported; untested signed/negative-zero formats remain untested. Internal validation ordering is not established. Prose issues scored separately.

One-repair prompt supplied under the same policy as T02-B: actual passing execution summary, unchanged task, missing exact-result-type assertion and accurate concrete mapping/limitations. No evaluator source or demonstrations disclosed. After-one-repair acceptance: **PASSED**. The repaired suite passes all 15 reference tests, detects all 5/5 fixed mutants, and explicitly asserts exact built-in int output. See `repair-01/RESULT.md`. This completes the development comparison.
