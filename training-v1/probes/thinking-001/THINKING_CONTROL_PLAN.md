# Thinking control 001 — declared before generation

2026-11-04. Local RTX 3080 only. No optimizer updates, model conversion, LM Studio
changes, cloud access, final or regression tasks. Preserve all prior artifacts.

Compare frozen pinned NF4 base, qwenny-001 E5, and qwenny-002-compact E5 on only
the already-visible DV001/DV002 instruction-only messages saved in gap-001.
E5 is the predeclared endpoint for both trajectories, not a selected winner.
Verify pinned base manifest and both stored fresh-import logit probes.

Thinking enabled through the pinned tokenizer template. Seed 42 reset per cell;
temperature 1, top_k 20, top_p .95, presence penalty 0, repetition penalty 1.
One first attempt per cell, six total. Order base/original/compact for DV001,
original/compact/base for DV002. Same exact rendered prompt within each task.
8192 new tokens shared by reasoning and final answer, context ceiling 16134,
no prompt truncation. Explicit im_end/endoftext stops. No retries, repairs,
best-of-N, cap increase, or development-output training targets.

The larger cap is declared for this thinking-mode control; comparisons to old
2048-token direct-answer results are confounded by budget. Presence zero matches
the recent sample0 controls. This is not a replication of historical GGUF/LM Studio
thinking with presence 1.5 and unrestricted responses. No precision causal claim.

Save full raw output and token IDs, prompts, timing, memory, reasoning closure,
reasoning/final token counts, termination/truncation, and final code-block count.
Never extract reasoning code as a final answer if the thinking delimiter is absent.
Inspect all final candidate source and hash-bind approval before unchanged isolated
reference/three-mutant evaluator execution. Review original explicit contract
coverage and prose separately for strict acceptance. Reference-invalid outputs
get no mutant credit. Truncation remains a failure, including no final answer.
Report all cells and limits; two families/one seed cannot establish general aptitude.
