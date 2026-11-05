# Frozen local S009 resource diagnostic (proposed; run on the training PC)

This is a diagnostic, not a training study. Its checkpoints are written to a temporary folder and deleted. Nothing here is an S009 endpoint or a model-quality result.

`run_diagnostic.py` records this file's SHA-256 in every run ledger. If this file is edited, that is a new protocol.

## 1. Question

When the S009 baseline workload runs for its full length, does it stall again? If it does, which single change prevents the stall: allocator settings, batch order, cache release at checkpoints, a memory cap, or the removal of other GPU consumers?

## 2. Fixed workload

The workload is the S009 baseline packet: `studies/S009-value-comments/preparation-001/baseline`, 60 training and 24 development rows. Each condition runs 5 epochs, which is 300 microbatches. All other settings match `train_s009.py`:

- Shuffle with `random.Random(42+epoch)`, batch 1 with gradient accumulation 4.
- AdamW: learning rate 1e-4 with a 3-update warmup, weight decay 0.01, gradient clip 1.0.
- Rank-4 LoRA on the 16 q/v projections; NF4 base; BF16 input embedding on the CPU.
- 128-token checkpointed chunked loss.
- After epochs 1, 3 and 5: save the adapter and optimizer state, then run 24 no-grad development losses.

The base model, tokenizer and package environment are unchanged. Use the existing `lora-feasibility` venv and `training-v1/runtime.py`; no code under `training-v1/` or `studies/` is modified.

## 3. Conditions

Each condition changes exactly one thing relative to C0. Every condition runs in a fresh process, in this order:

| ID | Single change |
|---|---|
| C0a | none (control) |
| C1 | `PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:256`, set before CUDA starts |
| C2 | length-descending order within each epoch (diagnostic only: this changes the trajectory) |
| C3 | `gc.collect()` + `torch.cuda.empty_cache()` after each checkpoint and development evaluation |
| C4 | `torch.cuda.set_per_process_memory_fraction(0.80)`, a cap of ≈8.59 GB |
| C5 | **the user** closes or unloads approved GPU apps (for example, unloads the LM Studio model) before the run. Included only with `--c5-confirmed`. The script never closes anything. |
| C0b | none (repeated control, to bracket drift during the session) |

## 4. Telemetry and stopping

- **Per microbatch:** seconds, allocated, reserved, peak allocated, peak reserved, `mem_get_info` free memory, `num_alloc_retries` and `num_ooms`. Checkpoint start and end events are logged too.
- **Every 0.5 s:**
  - `nvidia-smi` device used/free memory, plus `--query-compute-apps` per-process memory;
  - Windows `GPU Process Memory` dedicated and shared counters for **every** process, not only the trainer.
- **Startup gate:**
  - At least 10 counter rows for the trainer's own PID must appear within 60 s.
  - Otherwise the condition is recorded as `telemetry-invalid` and carries no evidence.
  - This fixes the S009 failure mode where the counter file had zero usable rows.
- **Watchdog:** a condition stops if either of these happens:
  - a microbatch exceeds max(30 s, 10× the median of the previous 20 microbatches; 120 s before any history exists);
  - free memory stays below 128 MiB for more than 30 s.

  A checkpoint step stops if it exceeds 300 s. A watchdog stop ends only that condition.
- **Ceiling:** 1,800 s per condition, including model load. This is 1.65× the nominal ≈1,080 s (about 180 s load and checks, plus 300 × 2.7 s, plus 3 × 30 s). There is a 120 s idle gap between conditions, so the whole run takes at most ≈3.6 h.

## 5. Frozen interpretation

- Telemetry-invalid conditions are excluded and reported as such.
- If **neither control** stalls (no watchdog stop, no ceiling, minimum free memory ≥ 128 MiB), the stall did not reproduce. Mitigation results are then **uninformative**; report them only descriptively.
- If a control stalls, a mitigation counts as a success only if it completes all 300 microbatches with no watchdog stop and minimum free memory ≥ 256 MiB.
- If only C5 succeeds, external GPU consumers are implicated.
- If C4 ends in an OOM error, our own demand exceeded the cap. Report it, and do not raise the cap within this study.
- Any successful mitigation must be replicated in a separately declared run before a future paired training attempt depends on it.

## 6. Commands

From the repository root, on the training PC:

1. Dry run (CPU only; checks orchestration, telemetry handling and the watchdog; writes under `diagnostic/runs/*-dry`):

   ```bash
   python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --dry-run --ceiling 60 --idle 1
   ```

2. Real run of C0a, C1, C2, C3, C4 and C0b (C5 is skipped):

   ```bash
   python independent-review/s009-slowdown/diagnostic/run_diagnostic.py
   ```

3. Optional, after you have closed approved GPU apps yourself:

   ```bash
   python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --only C5 --c5-confirmed
   ```

4. Summary table and frozen verdict (also produced automatically at the end of each run):

   ```bash
   python independent-review/s009-slowdown/diagnostic/summarize.py independent-review/s009-slowdown/diagnostic/runs/<stamp>
   ```
