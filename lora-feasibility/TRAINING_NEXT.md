# Next stage: local 3080 task-training pilot

User selected the local RTX 3080 on 2026-11-03. Do not switch to cloud or incur rental costs.
Native Windows stack, pinned upstream revision, and earlier experiment controls remain recorded in RESULTS.md.

Latest measured update: `REAL_LENGTH_RESULTS.md`. A 768-token ten-update trial with
checkpointed chunked loss passed at approximately 2 seconds/update, with 82 MiB
peak sampled process shared usage during updates. For the hypothetical 60-example,
three-epoch pilot, allow 15–30 minutes for the training/checkpoint stage provisionally;
dataset preparation/review and evaluation are separate. Memory remains limited.
The timing scenarios below are retained planning arithmetic, superseded by that
measured configuration where its assumptions apply. No task-training corpus is frozen yet.

## Dataset readiness

Existing D01/D02 are training candidates, not a frozen approved training corpus.
They have executable reference/mutant checks and bounded oracle evidence; independent
review remains pending. No failed model responses or evaluation answers are approved targets.
Profiled with the pinned tokenizer, current system prompt, full specification and
ANSWER.md, using an explicit thinking-disabled formatting candidate:

| Candidate | Family | Full chat tokens | Answer tokens |
|---|---|---:|---:|
| D01 | Integer ceiling division | 767 | 466 |
| D02 | Literal prefix removal | 752 | 445 |

The profile is saved in candidate-token-profile.json with source hashes. This is
not a training export, and thinking-disabled formatting has not been selected for
the eventual quality experiment. Preserve/review the reasoning policy explicitly
before training; historical inference controls still have thinking enabled.

The protocol's planning targets are 60 training tasks, 12 development, 24 final
held-out and 12 separate regression tasks, split by independent problem family.
These are task counts, not evidence of statistical power. Allocate family IDs and
splits before writing variants. Do not silently promote visible development tasks
or the prompting comparison tasks into unseen final evaluation.

## Local capacity and duration gate

The previous 64/128-token synthetic trials passed but do not establish that full
examples fit. A separate 768-token synthetic trial matches the longest of the two
current candidates without training on either. This remains a capacity/timing probe.
If it fails or has negligible margin, fix/measure memory at full-example lengths
before task training. Do not truncate target pytest files just to fit the GPU.

After dataset freeze and full-example fit, benchmark representative complete
examples on this exact machine. Record warmup separately and use multiple timed
microbatches, including gradient accumulation and optimizer work.

For un-packed, batch-one training of 60 examples for 3 epochs:

- 180 forward/backward microbatches, assuming one sequence per example and no dropping.
- With accumulation 4: roughly 45 optimizer updates; accumulation does not reduce
  the 180 microbatches of work.
- Compute estimate = measured seconds per representative microbatch x 180, plus
  optimizer overhead not included in that measurement, loading/checkpoints and evaluation.
- At a hypothetical 5 seconds/microbatch: 15 minutes of microbatch computation.
- At a hypothetical 20 seconds/microbatch: 60 minutes of microbatch computation.
- These scenarios are arithmetic, not measured timing predictions for this GPU.

The two-second 128-token synthetic update must not be extrapolated directly to
768-token examples, different adapter scope, BF16, a 4090, or multiple epochs.
An initial scheduling allowance of a few hours includes setup/pilot/evaluation,
not dataset authorship and independent review. Refine after real-length benchmarking.

## Task-training run contract

Freeze source records, reviewed assistant targets, tokenizer/chat template, reasoning
policy, family split manifest and hashes before exporting JSONL. Verify assistant-only
loss masking with explicit nonzero target-token counts and no silent truncation.
Select epoch/step count on development data, not final tasks. Save adapter checkpoints
and evaluate matched base A/B and adapter controls in the same runtime/precision.
Treat LM Studio deployment/merge/requantization as a separate experiment.

No meaningful task-training run has started yet. Synthetic feasibility adapters
are disposable and must not be used as candidate Qwenny improvements.
