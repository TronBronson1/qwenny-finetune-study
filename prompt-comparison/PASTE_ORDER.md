# Manual Qwen comparison

The user operates Qwen and returns complete responses in this chat. Codex manages files, runs tests, records scores and prepares any one-repair feedback. Do not automate LM Studio for this workflow.

Keep the existing system prompt and all current load/inference settings fixed. Use seed 42 throughout this initial comparison. Each initial request gets a fresh empty chat. Retain each chat for its possible single repair.

Paste the entire contents of each packet as one user message, in this order:

1. `packets/T01-A.txt` — rotation, instructions only.
2. `packets/T01-B.txt` — same rotation task plus both checked demonstrations.
3. `packets/T02-B.txt` — clock parsing plus both checked demonstrations.
4. `packets/T02-A.txt` — same clock task, instructions only.

Return each complete first response labeled with its packet ID before requesting any correction. Include displayed generation time, token count and stop reason when available; report any cutoff or context overflow. Codex scores the first response, then provides one repair prompt only if needed. Paste that repair into the original chat and return the entire corrected answer labeled `repair-01`. Do not add hints or retries independently.

Both demonstrations are already included in B packets. Do not paste them into A chats or add them separately to the system prompt. Do not show Qwen evaluation fixtures, evaluator tests, check logs or reviewed answers for the new tasks.

First-attempt and after-at-most-one-repair results remain separate. Passing first attempts retain a passing cumulative outcome without generating a repair. After this comparison, review results before proceeding to weight alterations. LoRA remains the first planned weight alteration.

Status: all four initial answers and all four one-repair answers scored. First-attempt strict acceptance: A 0/2, B 0/2. After at most one repair: A 1/2, B 0/2. T02-A's repair passed; comparison complete. Reports/logs are under `../runs/comparison-*/`; final table and limitations in `COMPARISON_RESULTS.md`. Next milestone: LoRA training feasibility, as described in `../02_MACHINE_AND_TRAINING.md`.
