# Qwenny local LoRA feasibility results

Date: 2026-11-03. This is a training-plumbing and measured-memory experiment, not a quality experiment.

Latest: user selected the local 3080. Additional 768-token trials and a ten-update
chunked-loss benchmark are complete. See `REAL_LENGTH_RESULTS.md` for shared-memory
measurements and the updated provisional training estimate. The two shorter trials
below remain preserved evidence, not the latest capacity/timing result.

## First actual 9B trial: passed, marginal memory headroom

Checkpoint: `Qwen/Qwen3.5-9B`, revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`.
All four full-precision source weight shards downloaded and SHA256-verified before local quantized loading.
Source weight tensor headers contain 9,653,104,368 parameters, including the vision tower.
The two untied 248320 x 4096 input/output matrices contain 1,017,118,720 parameters
each; kept in BF16, together they consume 4,068,474,880 bytes (about 3.79 GiB).

Runtime: native Windows, RTX 3080 10 GB, torch 2.14.1+cu126,
Transformers 5.22.1, PEFT 0.21.2, Accelerate 1.15.0, bitsandbytes 0.50.2.
Exact dependency locks, source script snapshot and report are in `runs/trial-001/`.
The separate synthetic 4-bit CUDA kernel preflight also passed; it is not counted
as the full-model result.

Configuration: NF4 frozen base with double quantization, BF16 computation,
SDPA full attention, PyTorch DeltaNet fallback, non-reentrant gradient checkpointing,
batch 1, sequence 128, rank 4, alpha 8, dropout 0, AdamW learning rate 1e-4,
one update. Only q_proj/v_proj in the eight full-attention blocks received adapters.
Exactly 557,056 trainable adapter parameters. No vision, MLP, embedding or DeltaNet
parameters trained. Selective preparation preserves BF16 input embeddings/output
head and upcasts other nonquantized FP16/BF16 weights; see script/report.

Evidence:

- Full model loaded on CUDA with no CPU/disk dispatch requested.
- Finite synthetic full-token loss: 0.5011269450.
- Adapter gradients were finite; at least one was nonzero, and no base parameter had a gradient.
- Optimizer changed adapter parameters.
- Adapter saved as `adapter_model.safetensors` (2,232,928 bytes) with configuration.
- Original model released, fresh base loaded, adapter reloaded.
- Checked last-token logits matched exactly (maximum absolute difference 0.0).
- The measured update region reported 2.0 seconds, excluding download, verification,
  model load, adapter save and reload. This single tiny run is not a throughput benchmark.

| Stage | Allocated GiB | Reserved GiB | Free MiB at stage |
|---|---:|---:|---:|
| Base loaded | 7.35 | 7.41 | 870 |
| Adapter ready | 7.36 | 7.41 | 944 |
| Forward | 7.52 | 7.82 | 581 |
| Backward | 7.38 | 7.95 | 484 |
| Optimizer | 7.39 | 7.95 | 558 |

Cumulative PyTorch peak allocated: 8,333,158,912 bytes (7.76 GiB).
Cumulative peak reserved: 8,535,408,640 bytes (7.95 GiB).
Across 177 whole-GPU samples, maximum used was 9714 MiB and minimum free was
340 MiB. Samples include verification, loading, step and reload, and external
desktop activity. They are not isolated process-only measurements and may miss
brief peaks. PyTorch allocator counters exclude allocations outside its allocator.
Windows shared-GPU-memory use was not separately measured. No long-run stability
or larger-context guarantee follows from this result.

The 340 MiB sampled minimum is below our approximately 512 MiB practical target.
Therefore the result is **mechanically feasible at this tiny configuration, with
marginal desktop headroom**. A separate 64-token trial investigates sequence savings.

## Second actual 9B trial: 64 tokens, also passed

`runs/trial-002-seq64/` uses the same script/configuration with sequence length 64,
in a fresh process, rechecking checkpoint hashes and performing another complete
load/forward/backward/optimizer/save/reload cycle. The same 557,056 adapter
parameters were trainable. Finite synthetic loss was 0.9906919599; checked reload
logits again had maximum absolute difference 0.0. The reported update region was
1.75 seconds, with the same timing limitations as trial 1. Losses at the two lengths
are not a quality comparison because the repeated token sequence/loss weighting differs.

| Trial | Sequence | Peak PyTorch allocated | Peak PyTorch reserved | Max sampled GPU used | Min sampled GPU free |
|---|---:|---:|---:|---:|---:|
| 001 | 128 | 7.76 GiB | 7.95 GiB | 9714 MiB | 340 MiB |
| 002 | 64 | 7.56 GiB | 7.73 GiB | 9647 MiB | 407 MiB |

Trial 2 contained 174 GPU samples. Different desktop activity and loading peaks
also affect whole-GPU minima, so the small headroom difference cannot be attributed
solely to sequence length. Both remain below the approximately 512 MiB practical
target. No further sequence reductions were attempted: model residency is the
dominant cost and more tiny synthetic trials would not establish useful training fit.
Both processes exited normally. Post-trial nvidia-smi reported 1483 MiB used,
8571 MiB free; the inference models/files were not modified.

Conclusion: the chosen native Windows 4-bit stack is **verified for these two tiny
training trials**, including adapter persistence. The desktop VRAM margin remains
marginal. Prefer a measured BF16 trial on a dedicated 24 GB GPU for the next
substantive stage if cloud rental is acceptable, rather than treating these
synthetic adapters as quality candidates. No cloud account, upload or rental was
created as part of this investigation.

## Interpretation and next steps

The disposable adapter learned one synthetic repeated chat sample, with thinking
disabled for that sample and loss on all tokens. It is not a Qwenny candidate and
has no measured task benefit. Historical LM Studio prompting controls remain intact.
Do not load this adapter as the next quality experiment.

Quantized LoRA trains higher-precision adapter parameters against an approximated
frozen base. Changes relative to BF16 may affect answers/reasoning, and deploying
the adapter on a different precision/quantization can introduce another mismatch.
Qwen3.5-specific Unsloth guidance cautions against 4-bit tuning because of larger
quantization differences. Those risks require matched runtime/precision controls,
not a conclusion that this adapter necessarily degraded the model.

Unsloth's roughly 22 GB BF16 LoRA figure is a setup-dependent estimate, not a
universal minimum. A dedicated 24 GB 4090 is a reasonable candidate for a short
BF16 LoRA trial, with memory remeasured on the selected Linux/Unsloth stack before
larger context/rank/scope. No cloud rental has been started. BF16 would remove the
4-bit base approximation from training, but it would not remove dataset quality,
overfitting or deployment/evaluation concerns. Export/merge/GGUF compatibility
remains untested.

After memory feasibility, prepare enough reviewed training/development/regression
data and repeat matched base controls in the eventual evaluation runtime. The
earlier demonstrations still await second-person review. The visible development
families cannot be treated as unseen final tests.

Primary sources:

- https://unsloth.ai/docs/models/qwen3.5/fine-tune
- https://huggingface.co/docs/peft/developer_guides/quantization
- https://huggingface.co/docs/transformers/model_doc/qwen3_5
