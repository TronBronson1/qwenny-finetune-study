# S008 — fixed-input expected-value diagnostic

Declared November 4, 2026, before generation. Execute only after S007 reference/mutant calibration and negative controls pass. No new optimizer training, final/regression content, deployment or cloud work.

## Question

Can the existing base, original E1 and original E5 compute expected outputs when the input cases are supplied, without also inventing test cases or writing pytest syntax? This is a component diagnostic, not the original adapter-adoption comparison and not a rescoring of S006.

## Fixed task/case selection

Use the same eight task IDs as S006: TR024/TR025/TR038/TR049 and DV008/DV004/DV011/DV007. From candidate-007's ordered valid-case list select indices 0, floor((n-1)/3), floor(2*(n-1)/3), n-1, independently per task. Save exact case IDs, arguments, reference/oracle-checked expected values and prompt hashes before generation. Training tasks are familiar; development is already exposed. No random-population inference.

Show the cleaned contract, input schemas and return description, followed by the four explicit argument tuples. Do not show expected values, gold test code, demonstrations or mutants. Ask only for a JSON array of the four return values, converting any tuple returns to JSON arrays. No worked-step or hidden-reasoning requirement. Save scoring answers separately from model prompts.

## Matched local inference

Pinned NF4 base revision c202236235762e1c871ad0ccb60c8ee5ba337b9a, unchanged runtime with CPU embedding; exact E1/E5 reload probes required. Same saved prompt/token IDs per task across arms. Alternate training/development task order and rotate base/E1/E5 arm order by task index. One greedy first attempt per cell, 24 cells, seed42 reset; thinking disabled, do_sample false, repetition1, presence0, max512 new tokens, context ceiling16134 without truncating prompts. Verified im_end/endoftext stops. No repairs, retries, extraction from reasoning, best-of-N or output-cap increase.

Require >=8GiB initially free for the existing loading guard. Local RTX3080 only. Soft per-cell180-second and total3600-second model preflight/generation limits, checked at token boundaries; model loading/file verification can overshoot that soft boundary and must be reported. Stop on unexpected exception/probe mismatch/OOM; preserve partial attempts and missing cells. Temporary process-scoped keep-awake only; no app closure or persistent power changes.

## Frozen graded scoring

Primary: per-case output-value accuracy, four planned cases per task/arm (32 per arm). Parse the complete terminated answer as JSON, optionally accepting exactly one enclosing JSON code fence as a separately flagged formatting deviation. Do not extract a convenient array from surrounding prose. Require an outer array of exactly four entries. Reject nonfinite JSON constants. Parse/length/truncation failures contribute zero correct cases and are reported separately; do not omit them from the denominator.

Compare structure and strings exactly after reference tuples are normalized to JSON arrays. For primary numerical-value accuracy allow finite int/float equality, but never bool as a number. Secondary typed accuracy additionally requires matching JSON numeric/scalar types. Report strict requested-format compliance separately (bare JSON, no code fence), parseability, completion, per-task all-four correctness and tokens/time/memory. This measures the supplied values, not exception coverage, test-design completeness or exact Python container types.

All gold reference and original oracle values for selected cases must agree before freeze. Keep model answers unchanged and never execute model-generated code. No adoption threshold or general ability ranking is justified by eight purposive tasks and one greedy condition. Do not directly attribute differences from S006 to a single factor: prompts, supplied cases, response format, decoding and budget differ.

## Decision branches

High supplied-value accuracy with poor free-suite performance is consistent with case selection/packaging/coverage being a bottleneck; it does not isolate a mechanism. Poor supplied-value accuracy also motivates a narrower numerical/contract-comprehension investigation before training. Mixed results require task-level analysis. Neither outcome automatically authorizes extra epochs or checkpoint adoption.
