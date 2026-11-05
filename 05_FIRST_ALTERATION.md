# First candidate behavior alteration: explicit argument tracing

Prepared November 3, 2026 after pilot 001 failed first-attempt, one-repair, and additional second-repair acceptance. User subsequently supplied an answer using this prompt; evaluated in `runs/pilot-002-system-prompt/RESULT.md`: 23 passed, 3 failed against the reference. User confirmed the earlier system prompt was blank. Prompt effectiveness remains unestablished.

One-repair update: the corrected response passed all 28 reference tests, detected all six mutants, and met the pilot requirements. See `runs/pilot-002-system-prompt/repair-01/RESULT.md`. This establishes successful feedback-assisted completion on the familiar pilot, not first-attempt reliability or generalization.

The second repair removed an exception-handling bug but constructed `(5, 5, 10)` in a test expecting reversed bounds. Candidate intervention: add concise reusable system instructions requiring explicit input tuples and tracing them against the contract.

This changes prompt context, not weights. It is a proposed additional prompting baseline before LoRA. Keep it separate from arm B's planned two demonstrations. Do not claim it improves accuracy until measured on new development tasks. Reusing clamp_integer now measures repair/familiarity, not unseen-task performance.

## Candidate system prompt v1

Write simple, executable Python code that follows the supplied contract exactly.

For parametrized tests, write complete explicit argument tuples; unpack them directly. Keep ordinary return-value cases separate from expected-exception cases. Do not build argument lists through conditional expressions or duplicate tuple elements implicitly.

Before returning a test file, check each case against its concrete argument values and required result or exception. For a reversed-bounds test, verify that the actual lower value exceeds the actual upper value. When isolating an invalid input, hold the other arguments valid. Match every parametrized name to a test argument; request fixtures only when they are supplied. Use the exact requested import.

Distinguish tests you inspected from tests you executed. State limitations precisely; do not claim completeness or that one exception-order case proves every validation ordering.

## Controlled use

The user confirmed the prior system prompt was blank. In a separate LM Studio preset, keep all baseline loading/sampling values unchanged and add only this instruction text. Save exact rendered input when available. Compare the original and altered prompts on new development tasks in fresh chats, using matching seeds and scoring. Do not apply this to final held-out families during development.

If the next intended alteration is specifically learned weights, use the LoRA feasibility steps in `02_MACHINE_AND_TRAINING.md` and reviewed data rules in `03_DATASET_RULES.md`; this prompt is neither a trained adapter nor a substitute for that experiment. No training stack or memory-fit trial has yet been validated.
