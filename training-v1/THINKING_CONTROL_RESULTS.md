# Thinking-enabled control 001 results — 2026-11-04

Completed locally on the RTX 3080. Base, original E5 and compact E5 each scored **0/2 strict accepted**. No candidate selected. Existing models and prior experiment results were preserved; final and regression tasks remain untouched.

## Matched protocol

Pinned Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a, existing NF4/BF16 CPU-embedding runtime. Both E5 adapters reproduced saved probe logits exactly (max abs difference 0). Only the already-visible DV001 rotation and DV002 clock instruction-only messages were used. Rendered prompts and token counts matched within each task.

Thinking on; seed42 reset per cell; temperature1/top_k20/top_p.95; presence0/repetition1; 8192 total new tokens shared by reasoning and answer, context ceiling16134, explicit im_end/endoftext stops. One first attempt per cell. No prompt truncation, repairs, inference retries, best-of-N or cap increase. Protocol was saved before generation in THINKING_CONTROL_PLAN.md.

This is a bounded Python-runtime control, not historical unrestricted LM Studio GGUF with presence1.5. Comparisons with old thinking-off cap2048 results change both thinking and budget and cannot isolate thinking alone.

## All first attempts

| Task | Model | Total tokens | Before thinking close | After close | Terminated | Final block | Strict accepted |
|---|---|---:|---:|---:|---|---|---|
| DV001 | base | 8192 | 7246 | 945 | No, cap | Yes | No |
| DV001 | original-e5 | 6904 | 6461 | 442 | Yes | Yes | No |
| DV001 | compact-e5 | 8192 | no close | 0 | No, cap | No | No |
| DV002 | original-e5 | 8192 | no close | 0 | No, cap | No | No |
| DV002 | compact-e5 | 8192 | no close | 0 | No, cap | No | No |
| DV002 | base | 8192 | 7829 | 362 | No, cap | No | No |

Counts after the closing delimiter include any final stop token. Reasoning never closed in three cells; those cells have zero final-answer tokens, not zero reasoning tokens. Five of six responses hit the cap. The only terminated response was original E5 rotation, which failed collection.

## Execution and review

Every complete final candidate was read and hash-bound before unchanged isolated reference/three-mutant pytest execution. Reasoning code was never extracted as a final answer. Both executable candidate files failed the correct reference, so neither is eligible for mutant-detection credit. No incomplete code was repaired or executed.

- **DV001 / base:** Truncated after a complete code block; 24 reference tests fail because supposed valid/nonmutation inputs are lists, not exact tuples. Additional wrong negative-rotation and identity expectations; mapping truncated.
- **DV001 / original-e5:** Complete response, but collection fails with NameError: nested is undefined. Additional flattened argument/expected parametrization, invalid exception classes and identity assertions.
- **DV001 / compact-e5:** All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.
- **DV002 / original-e5:** All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.
- **DV002 / compact-e5:** All 8192 tokens consumed before closing the thinking section. No final answer or candidate file.
- **DV002 / base:** Thinking closes, but the final code truncates at an unfinished assignment with no closing fence or mapping. Visible code also expects TypeError for malformed exact strings, which require ValueError.

The initial scoring launch mistakenly used the model environment, which lacks pytest. Those infrastructure logs remain under scoring/thinking-001 and are excluded from quality evidence. The same saved candidates were then scored with the established Python3.15 / pytest9.2 interpreter under scoring/thinking-001-pytest. No generated answer changed. The unchanged evaluator retains a generic direct-answer scope string; the plan, generation report and this report specify the actual thinking-enabled run.

## Runtime and evidence

Six generations produced 47,864 tokens and took 6837.170 seconds (114.0 minutes), excluding loading, base verification, probe checks and scoring. The first base rotation generation was unusually slow. Timings include local runtime/memory conditions and do not isolate adapter effects.

Torch peak allocated 7.38 GiB / reserved 7.44 GiB. GPU-wide sampled minimum free memory was 68 MiB. Windows per-process memory counters produced no samples; shared-memory spill is unverified. No OOM was reported. The generation process exited successfully and its temporary keep-awake request ended.

- probes/thinking-001/: raw outputs, token IDs, final answer extraction, exact prompts, hashes, reload/consistency checks, timing and GPU logs.
- scoring/thinking-001-pytest/: definitive unchanged execution logs and agent-acceptance-review.json.
- thinking-control-results.json: complete machine-readable comparison.
- thinking-control-sha256.json: artifact fingerprints.

## Interpretation

Thinking enabled did not produce an accepted answer in this bounded control. Long repetitive reasoning consumed most or all of the budget, while the two complete final files remained contract-invalid. This does not prove that a larger budget would help, that training universally helps/harms, that 4-bit precision caused the failures, or that historical LM Studio behavior is reproduced. Two visible families and one seed cannot rank general aptitude.

Retain all candidates without adopting a winner. Freeze any next development protocol separately. Do not increase this run's cap, rescue these outputs, use failed development outputs as targets, or open final-test families to choose a candidate. No optimizer updates, cloud work, GGUF conversion or LM Studio changes occurred.
