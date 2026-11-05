# T02-B: after one repair

Executed unchanged with Python 3.15.0 / pytest 9.2.0: **16 reference tests passed; all 5/5 fixed mutants detected** through relevant assertions or expected-exception failures. Reference-valid, mutant score eligible. Full logs and exit codes preserved in `evaluation/`; complete user answer in `response.md`.

Strict task acceptance: **FAILED: exact built-in int assertion still missing**. The repair adds `isinstance(result, int)`, which accepts subclasses. For example, a locally defined `class IntChild(int): pass` produces a result `IntChild(720)` satisfying both `isinstance(result, int)` and `result == 720`. The original contract requires exact built-in int, so `type(result) is int` is needed. This is a review finding about an explicit original requirement, not an added frozen mutant or execution failure. The fixed five-mutant score remains 5/5.

Prose: mapping incorrectly claims isinstance proves exact type. It also labels `1-00:00` and `abc:def` non-ASCII even though both contain only ASCII characters. Their wrong lengths alone mean these examples cannot isolate delimiter validation. The mapping is otherwise more concrete, and limitations correctly avoid claiming knowledge of internal validation order or execution. The repeated external check-record reference does not identify a record produced by Qwen. Shape/sign coverage remains limited as noted for the first attempt; no new requirements or fixed mutants added during scoring.

User-operated settings, exact submitted request and fresh-chat state not independently verified; intended repair request retained. Timing, token count and stop reason not supplied.

One allowed repair exhausted. T02-B is complete: first-attempt and after-one-repair strict acceptance both failed despite reference validity and 5/5 mutant detection at both stages. Next: T02-A in a fresh chat, unchanged system prompt/settings and seed 42, no demonstrations or prior feedback included.
