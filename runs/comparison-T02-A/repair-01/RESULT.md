# T02-A: after one repair

Task acceptance: **PASSED** under the frozen code/coverage rubric. Python 3.15.0 / pytest 9.2.0: **15 reference tests passed; all 5/5 fixed mutants detected** through relevant assertions or expected-exception failures. The repair now checks `type(result) is int` and numeric equality on all three valid cases. Original response, extracted code, intended repair request, fixture logs and exit codes preserved.

Required sampled categories remain present: midnight, interior time, end of day, hour/minute bounds, malformed field widths, whitespace, Unicode digits, invalid types and actual str subclass. Source/file inspection, mocking or replacement is absent. No reference failures or collection errors. This is the single allowed repair; no further scored generation needed.

Prose review: mapping and limitations are valid Python comments inside the code block rather than separate prose after it; this is a presentation deviation, not one of the frozen executable acceptance gates. No fabricated execution claim or unsupported internal-order claim. Coverage limitations acknowledge finite inputs. Signed-zero and negative-hour strings are untested; their behavior is specified as rejection by the contract, so the wording about implementation-dependent parsing should not imply contractual ambiguity. There are no same-length wrong-delimiter/ASCII-nondigit cases; these remain disclosed coverage limitations, as for the other clock suites. Acceptance is not a claim of exhaustive coverage.

User-operated settings, exact submitted repair request and fresh-chat conditions not independently verified. Intended seed: 42. Timing/tokens/stop reason not supplied.

The initial A response failed strict acceptance because exact result type was unasserted; after one repair it passes. This completes the two-task development comparison. See `../../../prompt-comparison/COMPARISON_RESULTS.md` for both arms; these results cannot establish broad training or prompting effects.
