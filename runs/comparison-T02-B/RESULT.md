# T02-B: first attempt

Arm B, two fixed demonstrations. Answer returned by the user after the T02-B fresh-chat request. Intended packet saved; exact submitted input, fresh-chat state and effective settings not independently confirmed. Seed 42 and unchanged settings requested. Time/tokens/stop reason not supplied.

Executed unchanged with Python 3.15.0 / pytest 9.2.0: **16 passed** against the reference. All **5/5** designated mutants detected through relevant test failures: arithmetic (12:00 and 23:59), hour boundary (24:00), minute boundary (23:60), string-subclass acceptance (StrChild), Unicode-digit acceptance (Arabic-Indic zero digits). Mutation score eligible because reference passes. Logs and exit codes retained in `first/evaluation/`.

Strict first-attempt task acceptance: **FAILED: missing exact-result-type assertion**. The original task explicitly requires an exact built-in int. `== expected` permits equal-valued floats or int subclasses, and the mapping's int claim supplies no assertion. The five fixed mutants do not probe this requirement; passing them does not override the all-required-categories acceptance rule. This is a coverage failure, not a reference execution failure.

Coverage present: midnight, end of day, interior time, hour/minute bounds, malformed shape/length, leading/trailing whitespace, Unicode digits, invalid types and actual str subclass. Shape coverage is limited to wrong-length strings; there is no same-length wrong delimiter or ASCII nondigit case, and no direct sign example. These limitations are recorded without expanding the frozen mutant set or requiring exhaustive cases.

Prose: correctly distinguishes inspected from executed and avoids exhaustive claims. Mapping is generic rather than input-specific. It names an internal isinstance check without evidence and overstates internal validation-order conclusions. Observable TypeError outcomes are established, but internal operation order is not inspected. These prose issues are scored separately from code.

Single repair prompt supplied: add the missing exact-output-type assertion and correct the mapping/prose. Includes unchanged task and actual passing execution summary, no evaluator source or extra demonstrations. After-one-repair acceptance: **FAILED**. The repaired suite still passes 16 reference tests and detects 5/5 fixed mutants, but uses isinstance instead of an exact-type assertion. See `repair-01/RESULT.md`. T02-B is complete; next is T02-A in a fresh chat.
