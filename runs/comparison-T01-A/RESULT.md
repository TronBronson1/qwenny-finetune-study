# T01-A: first attempt

Arm A: instructions without demonstrations. User returned this response in the experiment chat. Intended packet saved separately; exact submitted input and effective settings have not been independently confirmed. Seed 42 and unchanged settings were requested. Timing, tokens and stop reason were not supplied.

Acceptance: FAILED. The file cannot be collected: line 85 has a required `steps` parameter following defaulted `values`. Python 3.15.0 / pytest 9.2.0 reports `SyntaxError: parameter without a default follows parameter with a default`. No test bodies executed. Reference validity fails; mutant detection is ineligible. All six fixture runs exit 2 with collection errors; none count as bug detection.

Static review also finds incorrect negative-rotation expectations; no assertions in the nested identity/mutation test; no actual duplicate-element case; missing tuple/int subclass cases; no invalid-step case with empty values; and an unsupported requirement that the outer result tuple be a different object. The positive modulo-zero expression itself yields the original tuple and is not an additional failure.

Prose: no affirmative fabricated execution claim. Identity coverage is overstated because no assertion establishes it. The limitation that nested identity was checked is inaccurate. Exact exception messages are not part of the contract.

Original response and extracted code preserved in `first/`. Execution evidence is in `first/evaluation/`. No edits or diagnostic fixes were applied to the scored answer. Single repair prompt prepared in `REPAIR_PROMPT.txt`, including unchanged specification, actual collection output and static unmet-category feedback. It reveals no hidden evaluator code or mutant source.

After-one-repair outcome: FAILED. See `repair-01/RESULT.md`: 32 passed, 3 failed against the reference. This exhausts the single allowed repair for T01-A. No B-arm answer received yet. No inference about demonstration effectiveness is possible from this result alone.
