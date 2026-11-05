# Qwenny handoff: first real adapters trained, import-verified, pilot negative

Date: 2026-11-03, America/New_York. User explicitly authorized local training and
multiple candidates after corpus review and the 2048-token fit check. Stay on the
RTX 3080; no cloud rental/upload/account was created. User operates LM Studio.
Preserve base models, prior prompting results, dataset snapshots and all run evidence.

## Start here

Read training-v1/README.md, training-v1/PLAN.md and training-v1/RESULTS.json.
Current run: training-v1/runs/qwenny-001. All jobs have completed and exited.
Temporary keep-awake requests were process-scoped; no persistent power-plan/display
setting was changed. No apps were closed/paused or LM Studio chats automated.

## What was trained

One fixed seed-42 trajectory, checkpoints after epochs 1, 3, 5. These are not
independent training runs or verified aptitude tiers. Ready adapter packages:

- training-v1/candidates/qwenny-001/Qwenny-E1
- training-v1/candidates/qwenny-001/Qwenny-E3
- training-v1/candidates/qwenny-001/Qwenny-E5

Each has adapter_model.safetensors (2232928 bytes), exact adapter_config.json copy,
SHA256s, base revision and provenance. Fresh-process imports reproduced each
stored probe's logits exactly (max absolute difference 0.0).

Pinned Qwen/Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a;
torch 2.14.1+cu126, Transformers 5.22.1, PEFT .21.2, bitsandbytes .50.2.
NF4/double quantized frozen base, BF16 computation, input embedding explicitly
in CPU RAM. Output head/transformer/adapters CUDA, non-reentrant checkpointing,
128-token chunked loss. Rank 4/alpha 8 query/value adapters in eight full-attention
blocks, 557056 trainable parameters. AdamW 1e-4, accumulation four, clip one,
three-update warmup then fixed rate. See PLAN/source snapshots for all settings.

60 training tasks x five passes = 300 microbatches / 75 optimizer updates.
Every task appeared exactly five times; no development/final/regression target
entered optimizer training. Elapsed optimizer training plus checkpoint development
evaluation: 694.968 seconds (11.6 minutes), excluding setup/base controls/probes.
All checked gradients finite/nonzero and limited to intended adapters; every
optimizer update changed adapter weights. Base files were not modified.

## Approval, formatting and preflight

Dataset candidate-006 hash:
9ebcef8e0ad4dcf498afc5fde3a2a1c34517458ca2639d705e8a0ad04e1c4d9f.
User corpus review and training authorization are recorded in
dataset-v1/USER_TRAINING_AUTHORIZATION_2026-11-03.json. The exporter supports this
explicit hash-bound corpus approval without inventing per-record reviewer actions.
Old per-record approval remains supported; unapproved/wrong-hash exports still
reject (training-v1/export-authorization-checks.json). Do not ask for the same
training approval again merely because immutable snapshot placeholders say pending.

Approved export: dataset-v1/training-approved-001. Tokens: training-v1/prepared-001.
Every supervised span decodes exactly to the authored visible answer plus im_end;
prompt/role/empty reasoning wrapper masked. No truncation; max input 1954.
This is direct-answer SFT, not reasoning-trace training or a guarantee of preserved
thinking. Historical LM Studio thinking-enabled settings remain unchanged.
Tokenizer im_end 248046 and endoftext 248044 were verified; generation stops on both.

Actual longest-example backward, masked standard/chunked loss/gradient comparison
and a cached-generation smoke check passed before optimizer training.

## Loss versus actual pilot behavior

Mean per-example development assistant-token losses:

| Weights | Instruction only | Two fixed demonstrations |
|---|---:|---:|
| Base | .8934 | .7899 |
| E1 | .7698 | .7082 |
| E3 | .3816 | .4306 |
| E5 | .1329 | .2218 |

These teacher-forced numbers are not task acceptance. They fell substantially,
while free-running correctness remained poor.

Secondary generation pilot:
training-v1/probes/qwenny-001-direct-001.
Two visible development families DV001 rotation / DV002 clock, seed 42.
Thinking OFF, max_new_tokens 2048, temperature 1, top_k20, top_p.95, output-only
presence penalty1.5. This is explicitly separate from historical thinking-on,
uncapped LM Studio controls. One first attempt per variant/task; no repair/retry.
Base A/B and E1/E3/E5 C were matched in this Python runtime.

Execution:
training-v1/scoring/qwenny-001-direct-001/summary.json and agent-acceptance-review.json.
All complete code blocks were read, hash-bound inspection logged, then executed
against isolated reference/mutant fixtures. Results:

- Base A: 0/2 reference-valid, 0/2 agent strict accepted.
- Base B: 0/2 reference-valid, 0/2 agent strict accepted.
- E1: clock reference-valid and 3/3 designated mutants detected, but missing exact
  built-in int output coverage; 0/2 agent strict accepted.
- E3: rotation truncated without complete code block; clock collection failure;
  0/2 accepted.
- E5: rotation syntax errors; clock wrong exceptions/arity; 0/2 accepted.

E1 clock diagnostic: a non-bool int-subclass return implementation passed all
24 generated tests, whereas gold detected it. This post-hoc check diagnoses an
existing explicit requirement; it was NOT added to the frozen three-mutant score.
See training-v1/diagnostics/qwenny-001-exact-int-gap.

No accuracy gain is demonstrated by this limited pilot. Do not select/adopt E5
just from its lower loss, claim general harm/benefit, or attribute errors to 4-bit
quantization without a controlled precision comparison. Two families/one seed
cannot rank general aptitude. Broader regression and all 24 final tasks remain
unmeasured by the trained models.

## Cache and deployment

Read-only diagnostic: training-v1/diagnostics/qwenny-001-cache-001. Compared cached
raw decoding logits with full-context forwards at five positions each for base/E5.
Top token matched 5/5 both; max KL .00190/.00123; raw logits not identical (max
abs .5625/.75). No gross mismatch at these checked positions, not an exhaustive
cache/numerical guarantee. Diagnostic greedy samples were not used as scored retries.

PEFT import is verified. These are NOT standalone LM Studio GGUFs. A separate
merge/conversion/requantization and matched deployed-base control is still needed;
the original GGUF's exact conversion lineage to the pinned training base is not
established. Do not silently apply adapters to an assumed-identical existing GGUF
or replace the working model. User continues to operate LM Studio.

## Sensible next work

Investigate teacher-forced likelihood versus generation behavior on development
data before blindly adding epochs or declaring a winner. Candidates include
properly matched thinking-enabled/decoding controls, a concise target-format
ablation and careful optimizer/scope trials. Any new configuration must be recorded
separately. Preserve first attempts, no best-of-N, no failed outputs as targets.
Keep final families untouched until protocol/candidate selection is frozen.
