# Pilot 002: accepted after one repair

November 3, 2026. User-submitted answer preserved in response.md and extracted unchanged to test_candidate.py. Execution: Python 3.15.0 and pytest 9.2.0; same reference and six mutants as the earlier attempts. Full logs and execution_summary.json saved here.

| Implementation | Result |
| --- | --- |
| Correct reference | 28 passed |
| M1: accepts bool/int subclasses | 9 failed, 19 passed |
| M2: skips upper type validation | 4 failed, 24 passed |
| M3: rejects equal bounds | 1 failed, 27 passed |
| M4: omits upper clamping | 2 failed, 26 passed |
| M5: omits lower clamping | 1 failed, 27 passed |
| M6: checks reversed bounds before types | 1 failed, 27 passed |

Reference-valid suite: yes. Required mutants meaningfully detected: 6/6. Prompt requirements reviewed: normal and negative ranges, below/above limits, distinct endpoints, equal bounds, reversed bounds, all six forbidden input types in all three positions, and the required mixed-invalid precedence case have executable assertions. No replacement/mocking or implementation inspection. Acceptance: PASS after one repair. First-attempt result remains a failure (23 passed, 3 failed).

Each mutant has a relevant assertion/expected-exception failure, not a collection error. The callable form of pytest.raises is valid. The MyInt helper is now at module scope; distinct endpoint tests are restored.

Reporting review: the model did not claim execution or exhaustive coverage. The mapping's first row associates several inputs with one method name, a minor imprecision; the other rows identify the actual relevant methods. "Specification only" is loose wording for executable, unexecuted tests, not a fabricated execution claim.

Interpretation: this reused development task succeeded with the candidate system prompt plus one explicit repair. Earlier blank-system-prompt attempts failed even after an additional second repair. This is an observed contrast, not a controlled estimate of prompt effectiveness: the new prompt was designed from these same failures, the task is reused, and exact complete requests/fresh-chat status have not been captured. Generalization and weight changes remain untested.

Close this repair cycle. Next evaluate the frozen prompt on new development task families using matched original/altered settings, or proceed to training feasibility/data preparation as a separately documented stage. Do not count this familiar task as held-out evidence.
