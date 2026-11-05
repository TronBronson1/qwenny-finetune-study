# Full-example length, Windows shared memory and local timing

Date: 2026-11-03, America/New_York. User explicitly chose to remain on the local
RTX 3080; no cloud rental, account or upload was created.

## Why the tiny trial was insufficient

Pinned-tokenizer profiling of the current system prompt, SPEC.md and ANSWER.md
produced 767 tokens for D01 and 752 for D02. Both remain training candidates with
independent review pending. The formatting profile explicitly disabled thinking;
this is not a decision to change the historical thinking-enabled inference controls.
No candidate example was trained in these trials. All trials below use the same
repeated synthetic chat tokens to test capacity and timing, not task quality.

## Three additional actual 9B runs

| Run | Length | Loss implementation | Updates | Update timing | Outcome |
|---|---:|---|---:|---|---|
| 003 | 768 | Standard model loss | 1 | 40.547 s | Passed update/save/reload; exhausted device headroom |
| 004 | 768 | Checkpointed loss, 128-token chunks | 1 | 1.828 s | Passed update/save/reload |
| 005 | 768 | Same chunked loss | 10 | 2.033 s mean; 1.945 s median excluding first two | Passed every update and save/reload |

Same pinned base/runtime and narrow rank-4 q_proj/v_proj adapter scope as the first
two trials: 557,056 trainable parameters. All gradients were finite, at least one
was nonzero on every update, no base gradients occurred, and every optimizer update
changed adapter parameters. All three checked reload logits had maximum absolute
difference 0.0. Source script snapshots, package locks, adapters, reports and memory
samples are preserved in their individual run directories.

### Standard-loss memory pressure

Run 003 peaked at 10,417,888,256 bytes PyTorch allocated and 11,047,796,736 bytes
reserved. CUDA reported zero free device memory at forward/backward/optimizer
stages. nvidia-smi samples reached 10027 MiB used, 27 MiB free. Successful execution
therefore does not establish a dedicated-VRAM-only fit. The user independently
reported seeing approximately 99% GPU utilization and about 1 GB of shared GPU
memory overage during the recent run. This is a user observation, not an automated
quantification or timestamp-aligned measurement of that run. It supports the
interpretation that Windows shared-memory spillover affected the 40.5-second timing.

### Chunked loss validation and memory

The variant applies the same next-token objective over all tokens; it does not
truncate targets. It calls the backbone, computes the output head and summed
cross-entropy in token chunks, checkpoints each chunk, and divides by the same
number of valid next-token positions. This limits large vocabulary-logit temporaries.
Save/reload checks request only the final-token logits, the only logits compared.

Before the timed update, a 64-token comparison used the standard loss and a
32-token-chunk version. Loss values were 0.9906919598579407 versus
0.9906920194625854. Relative L2 difference across adapter gradients was about
1.5723%, below the predeclared 3% tolerance. Gradients were not bit-identical;
BF16 arithmetic/reduction order can differ. This is bounded numerical validation,
not a proof of exact equivalence for every input/length or assistant-only mask.
At 768 tokens, initial losses were 0.0880229473 (standard) and 0.0880229399 (chunked).
Synthetic loss decreases across repeated updates are not evidence of task improvement.

Run 004 peak allocated/reserved: 8,648,376,320 / 8,766,095,360 bytes.
Minimum stage CUDA free: 232,333,312 bytes; minimum sampled nvidia-smi free: 675 MiB.

Run 005 peak allocated/reserved: 8,655,060,992 / 8,772,386,816 bytes.
Minimum stage CUDA free: 181,452,800 bytes (173 MiB); minimum sampled nvidia-smi
free: 545 MiB. These APIs measure different aspects/times under WDDM; do not combine
them as exact whole-device accounting or claim abundant memory margin.

Windows GPU Process Memory counters were sampled for the training PID. The initial
monitor stopped on a transient invalid counter sample, retained in its error log.
The resumed monitor skips invalid samples. Thirteen valid samples fell between
adapter-ready and optimizer update 10. Peak process shared usage in that interval
was 85,983,232 bytes (82 MiB), with dedicated usage 9,038,114,816 bytes. This did not
show the approximately 1 GB shared use reported for the standard run. Shared usage
is not necessarily all paging; driver mappings/staging can contribute. Sampling
about every 1.5 seconds can miss short peaks. The run is only about 20 seconds of
updates, not proof of hours-long stability or larger contexts/scopes.

Both training and monitoring processes exited. Post-run nvidia-smi reported 880
MiB used and 9174 MiB free. Other applications were not terminated.

## Timing estimate and remaining work

Run 005 times (seconds): 2.156, 2.266, 1.906, 2.141, 1.937, 1.953, 2.219, 2.078,
1.828, 1.844. Total 20.328 seconds; mean 2.0328. Excluding first two, median 1.945.
See timing-summary.json for the calculation and real-length-summary.json for runs 003/004.

For a hypothetical 60 examples x 3 epochs, one 768-token sequence per example,
batch 1 and the same adapter/loss configuration: 180 microbatches x 1.945 seconds
is approximately 5.835 minutes of update computation. A provisional scheduling
allowance is 15–30 minutes for training/loading/checkpoint checks. This is not a
full-dataset benchmark or a promise: the corpus is not frozen, example lengths and
masking vary, desktop use can change, and model/loss settings may change after review.
Development/regression evaluation and dataset authorship/review are additional.
The earlier approximately two-hour arithmetic used the paging-affected standard
loss; it is not the estimate for this chunked configuration.

Meaningful task training has not started. Next assemble/review the planned family-
split corpus, freeze hashes and reasoning/formatting policy, verify assistant-only
masking with complete targets, and run matched base controls. The initial protocol
targets remain 60 training / 12 development / 24 final / 12 regression tasks.
Neither a two-example overfit run nor these synthetic adapters should be called a
Qwenny improvement. Keep deployment/merge/GGUF checks separate.
