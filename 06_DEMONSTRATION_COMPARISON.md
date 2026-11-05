# Next experiment: fixed instructions, with and without demonstrations

Prepared November 3, 2026. LoRA remains the first planned weight alteration. This experiment changes context only. No Qwen comparison results have been recorded yet.

## Fixed material

Use `prompt-comparison/SYSTEM_PROMPT.txt`, copied exactly from candidate system prompt v1 in `05_FIRST_ALTERATION.md`. Keep the current LM Studio load and inference settings in `04_LM_STUDIO_BASELINE.md`, including thinking on, temperature 1, top_k 20, top_p 0.95, presence penalty 1.5, context 16134, and seed 42. Do not revert to the earlier blank prompt. Record effective settings and model file/hash before treating a run as formal evidence.

Arm A receives shared instructions and the new task. Arm B receives the same shared instructions and task plus exactly the two fixed demonstrations in `prompt-comparison/DEMONSTRATIONS.md`, in D01/D02 order. Put examples in the user message; do not modify the system prompt. These examples are context, never evidence that Qwen ran tests.

## Checked demonstrations

| ID | Family | Reference | Designated bugs detected |
| --- | --- | --- | --- |
| D01 | Integer ceiling division / batch counts | 23 passed | 5/5 |
| D02 | One literal prefix removal | 23 passed | 5/5 |

See `prompt-comparison/CHECK_RESULTS.json` and each demonstration's `checks/*/pytest.log`. Checked with Python 3.15.0 and pytest 9.2.0. Authored and reviewed by Codex; independent human review is pending before training admission. These are training candidates, excluded from new-task comparison families and final held-out families. Full limitations accompany each answer. There is no exhaustive correctness or generalization claim.

## Paired development comparison

Use at least two new development families: sequence rotation and strict clock parsing. Freeze specifications, independent references, required categories, mutant implementations and witness inputs before requesting answers. Never show evaluator implementations, reviewed answers, or mutants to Qwen. Do not reuse clamp, discount, batch counting, or prefix-removal variants as new families.

Start with seed 42 in both arms without changing any other setting. Run a fresh empty chat for each task/arm. Alternate A/B order across tasks. For later variability checks, repeat with matching seeds 17 and 73 in fresh chats, changing only the seed in both arms. Save full exact messages, outputs, elapsed time, token information, stop reason, and effective settings. Context overflow or truncation compromises the pair; preserve the record and report it separately.

Score and archive each first answer before any feedback. Apply the acceptance rules in `01_EXPERIMENT_PLAN.md`: collectable suite, all reference tests pass, meaningful detection of every required mutant, and all required categories covered. Reference-invalid suites have no eligible mutant detection score. Review failures to distinguish real assertions from collection/import/runtime problems. Record prose accuracy separately.

For each failed first attempt, give exactly one repair in that same task's chat, retaining its arm's original context. Supply the unchanged specification and actual reference failure output; if reference-valid but coverage or mutants are missed, give a concrete unmet contract category without revealing mutant source. Use identical feedback rules in both arms. Return complete corrected file. No extra examples, coaching, or second repair. Preserve initial and corrected outputs separately. If the first attempt passes, report after-one-repair acceptance as passed without an additional generation.

Report first-attempt acceptance and acceptance after at most one repair separately, plus repair count, reference validity, eligible mutant detection, missing categories, unsupported prose claims, generation time, and operator effort. Compare paired wins/losses per task/seed and average within task before aggregating. Two development families are a workflow check, not a reliable estimate of broad accuracy. Keep final held-out families untouched.

## Status and continuation

Completed: two executable checked demonstrations, source files, review notes, logs, fixed prompt snapshot and file hashes. Also completed: two new development task packets (rotation and strict clock parsing), checked references and five mutants each, and a scoring tool verified on the rotation evaluator suite. Pending: Qwen generations and paired outcome scoring. The new references and suites are agent-reviewed; independent second-person review is pending. The local API at localhost:1234 refused connection when checked. LM Studio UI is available. No settings were changed and no Qwen answers were generated during preparation.


## Completed development comparison

All four initial answers and all four allowed repairs have now been scored. First-attempt acceptance: A 0/2, B 0/2. After at most one repair: A 1/2, B 0/2. No benefit from these demonstrations was observed on these two task families at intended seed 42; this is too small to generalize. Full results: prompt-comparison/COMPARISON_RESULTS.md. LoRA remains the first planned weight alteration; next is training feasibility, not an immediate full training run.
