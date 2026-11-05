# S009 slowdown forensics (independent analysis)

**Scope.** The S009 baseline arm stalled: Qwen3.5-9B NF4 QLoRA, rank 4, frozen BF16 input embedding on the CPU, chats of at most 2,048 tokens, RTX 3080 10 GB, Windows. This report uses only artifacts committed at `b0e0227`. It modifies no existing file and launches no GPU work.

Reproduce:

```bash
python3 independent-review/s009-slowdown/s009_forensics.py
```

The script needs only the standard library and matplotlib. It writes `outputs/microbatch-table.csv`, `outputs/analysis.json` and `figures/*.png`.

## 0. The most important limitation

The per-microbatch log, `training-v1/runs/qwenny-003-calibrated-baseline/events.jsonl`, is **not in the repository**. Neither are the 0.5 s `nvidia-smi` samples (`gpu-memory.csv`) or the Windows counter files. `.gitignore` excludes `training-v1/runs/`. Only their SHA-256 values are committed, in `studies/S009-value-comments/result-sha256.json`.

The committed record therefore gives only these:

- aggregates: 213 microbatches, 707.7 s in total, medians of 2.672 s and 34.352 s, training peak allocated and reserved memory;
- two preflight memory snapshots;
- one free-memory reading after termination.

The table in `outputs/microbatch-table.csv` reconstructs the microbatch sequence: epoch, position, task, input tokens, target tokens and optimizer step. Its time and memory columns are empty.

`python3 s009_forensics.py --run-dir <local copy of that run folder>` fills those columns from the local files. It checks each local file against the committed hash and asserts that every event matches the reconstructed task order. Running this on the training machine is the single cheapest way to turn most of the "guessed" rows below into "evidenced" ones.

## 1. Evidenced facts

| # | Fact | Source |
|---|---|---|
| E1 | The reconstructed order exactly reproduces the logged totals: 217,219 input tokens, 149,563 supervised tokens and 53 updates over 213 microbatches. The order uses `random.Random(42+epoch).shuffle` from `train_s009.py`. | `outputs/analysis.json` → `reconstruction.exact_match = true` |
| E2 | The batch that never finished is microbatch 214: epoch 4, position 34, **TR031, 1,188 input tokens**. It is the 15th-longest of 60 examples. | reconstruction |
| E3 | The two longest examples, TR049 (1,880 tokens) and TR058 (1,878), completed **seven times** before the stall: microbatches 52, 57, 71, 75, 142, 167 and 182. | reconstruction |
| E4 | Training peak allocated memory (7.53 GB) is *below* the preflight peak on the longest example (7.92 GB). Training peak reserved memory (8.120 GB) is within 4.2 MB (4 MiB) of the preflight reserved value (8.116 GB). PyTorch's reserved pool did not grow during training. | `stopped-evidence-001.json` |
| E5 | "Free = 0" with reserved ≤ 8.120 GB means that memory outside PyTorch's reserve reached **≥ 2.617 GB**. That memory is the CUDA context, non-allocator memory inside the training process, and other processes. At the preflights it was 2.233 GB (baseline) and 2.420 GB (comments). | accounting in `analysis.json`, `figures/memory_accounting.png` |
| E6 | The two preflights ran identical code with identical reserved memory, 223 s apart. Usage outside the reserve was **187 MB higher in the second one**. | preflight memory blocks |
| E7 | The training run passed the `load_base` guard (free ≥ 8 GiB, with its own CUDA context already open). Free memory read after termination was 8,138 MiB, which puts other processes at **2.204 GB with no training process alive**. That exceeds the 2.147 GB maximum the guard allowed even if the context were 0 bytes. **Other GPU consumers therefore grew by at least 54 MiB plus the training process's CUDA context during the arm.** With a context of 250 to 600 MiB that is 304 to 654 MiB, comparable to the 370 MiB (388 MB) of headroom the baseline preflight left. | RESULTS.md (post-run 8,138 MiB), `runtime.load_base` |
| E8 | The wall-time budget had little slack. Counting the pre-training phase (≈179 s, the same work as the preflight job), 300 microbatches at the positive-free median and three checkpoint evaluations, the undisturbed arm needs about **1,070 to 1,130 s against a 1,200 s ceiling**, roughly 6 to 11 % headroom. Four 34 s microbatches alone use about 120 s of it. | `analysis.json` → `time_budget` |
| E9 | The unfinished batch had been running for roughly **220 to 285 s** at the ceiling. That is 1,200 s minus the pre-training phase, the 707.7 s of logged microbatches and 30 to 90 s of estimated checkpoint work. A normal batch of that length takes ≈3 s. | `figures/time_budget.png` |
| E10 | On the same machine, step time collapses only at zero free memory. Feasibility trial-003 reserved 11.05 GB on a 10.74 GB card and took **40.5 s per step instead of 1.8 s**, with no OOM. The fit-2048 GPU-embedding run stalled for more than 2 minutes in backward, with sampled process shared usage of 0.66 GB. Every run with positive minimum free memory stepped in 1.8 to 4.3 s. | `lora-feasibility/*.json`, `figures/free_vs_step_time.png` |
| E11 | qwenny-001 ran on the same stack on Nov 3. It completed 300 microbatches and three checkpoint evaluations in 695 s, with median 2.0 s, minimum free 434 MB and a longest example of 1,954 tokens, longer than any S009 example. The compact run's minimum free was 801 MB. | `training-v1/training-summary.json`, `compact-trial-results.json` |
| E12 | S009's positive-free median (2.672 s) is 34 % slower than qwenny-001's (2.0 s), although per-pass supervised tokens are only ≈6 % higher. This is observed; its cause is not identified. | same |
| E13 | The training loop never calls `empty_cache()`. Checkpoints at epochs 1 and 3 run 24 no-grad development forwards of varying length between training microbatches. `Monitor` starts `nvidia-smi` every 0.5 s and a PowerShell counter script. | `train_s009.py`, `training-v1/runtime.py` |
| E14 | The Windows counter monitor wrote a header and zero rows. No `.error.txt` file was hashed, so the script stayed in its "fewer than 2 samples" branch or exited its loop immediately. | `monitor-process-memory.ps1`, result hashes |

## 2. Hypotheses

| Hypothesis | Verdict | Evidenced | Guessed / open |
|---|---|---|---|
| **Sequence length or a specific example** | Not supported as the cause | The stalled batch is mid-length, TR031 at 1,188 tokens (E2). The longest examples completed seven times (E3). Training never reached the preflight's peak allocation (E4). | Which four microbatches were zero-free is not in the repository. If they were 210 to 213, they were 694 to 1,066 tokens long. |
| **Allocator fragmentation or reserved-memory creep** | Not supported for PyTorch's pool | Peak reserved stayed at the preflight level, +4 MiB (E4). Creep inside the caching allocator would have raised reserved memory. | Fragmentation *within* the reserve without new `cudaMalloc` cannot slow the GPU this much. `num_alloc_retries` was not logged. |
| **Windows shared-memory fallback / WDDM paging** | Plausible mechanism, **not demonstrated for S009** | The machine shows this pattern elsewhere: over-subscription gives 20× slower steps without OOM (E10). S009's slowdown starts exactly when free memory hits zero. | No S009 shared-memory measurement exists (E14). The driver's sysmem-fallback policy setting is unrecorded. Eviction of this process's resident allocations, as opposed to new ones, is inferred, not observed. |
| **Checkpoint or evaluation timing** | Weak | E1's evaluation was followed by 120 normal microbatches. The stall came 33 microbatches after E3's. | A delayed effect of E3's 24 varied-length forwards cannot be excluded without the event timestamps. |
| **Other GPU consumers** | **Best supported** as what removed the headroom; the culprit is unidentified | Non-training GPU memory rose during the session (E6, E7). The run started with less headroom than qwenny-001 (E11). | Which process grew (LM Studio, the browser, the desktop compositor, `nvidia-smi` or the driver) is unknown. E6 could also partly reflect non-allocator differences inside the process. The 34 % slower baseline pace (E12) may be compute contention, which is unproven. |

**Most likely chain, labelled as inference.** The run started with only 0.2 to 0.4 GB of headroom, already less than on Nov 3. During the arm, memory used outside the training process grew until free memory reached zero. Windows did not fail with an OOM; it served the excess by paging to system memory, which slows every kernel touching paged memory by 10 to 100×. PyTorch never requested more memory, so a fixed-reserve workload became unstable. This fits every committed number, but neither the paging step nor the identity of the consumer is measured.

## 3. Frozen local diagnostic protocol (proposed)

Purpose: distinguish external growth from in-process causes, and test single-variable mitigations, before any new paired attempt. This is not a training study. Its checkpoints are discarded and are never S009 endpoints.

**Fixed workload.** Use the S009 baseline packet: same 60 records, seed-42 per-epoch order, rank 4, CPU embedding and chunked loss. Run 5 epochs (300 microbatches) with checkpoints after epochs 1, 3 and 5, under a new run ID. Every condition runs in a fresh process.

**Telemetry**, all written per microbatch and checked within the first 60 s, aborting the condition if any of it is missing:

- `torch.cuda.memory_stats()`: allocated, reserved, `num_alloc_retries`, `num_ooms`;
- `mem_get_info`;
- `nvidia-smi --query-compute-apps=pid,process_name,used_memory` together with device used/free;
- the repaired Windows `GPU Process Memory` dedicated/shared counters for **all** PIDs, not only the trainer. The startup check must see at least 10 trainer rows; otherwise treat the condition as invalid and do not just record "unavailable".

Record checkpoint and evaluation start/end events. Before and after each condition, record free memory and the list of other GPU processes.

**Conditions.** Each changes one variable relative to C0. Run them in the order C0a, C1, C2, C3, C4, C5, C0b. The repeated control brackets drift over the session.

| ID | Single change | Rationale |
|---|---|---|
| C0a / C0b | None (S009 settings) | Reproduce the stall and measure drift |
| C1 | `PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:256` | Allocator-side test. `expandable_segments` is not supported on Windows builds; if PyTorch warns, record it as not applicable. |
| C2 | Length-descending order within each epoch | Puts the peak first; diagnostic only, since it changes the trajectory |
| C3 | `gc.collect(); torch.cuda.empty_cache()` after each checkpoint and evaluation | Tests the checkpoint and evaluation hypothesis |
| C4 | `torch.cuda.set_per_process_memory_fraction(0.80)`, a cap of ≈8.59 GB | Turns silent paging into a fast, explicit OOM |
| C5 | The **user** closes or unloads approved GPU apps (for example, unloads the LM Studio model) before the run. The agent closes nothing. | Tests the external-consumer hypothesis directly |

**Watchdog.** For every condition, stop it and record a stall if any microbatch exceeds max(30 s, 10× the rolling median of the previous 20), or if free memory stays below 128 MiB for more than 30 s. A stall ends only that condition; the next one starts in a fresh process.

**Time limit.** Nominal work per condition is ≈180 s pre-training plus 300 × 2.7 s plus 3 × 30 s, about 1,080 s. Allow **1,800 s per condition** (1.65× nominal). That is ≤ 3.5 h for seven conditions, plus a 2-minute idle gap between conditions with free memory recorded. Do not reuse 1,200 s: on the S009 workload it leaves only 6 to 11 % headroom even with no slowdown (E8).

**Frozen interpretation:**

- If C0a and C0b do not stall, the stall did not reproduce. Report mitigation results as uninformative.
- Attribute a fix only if C0a stalls and a mitigation finishes all 300 microbatches with no watchdog trigger and minimum free memory ≥ 256 MiB.
- If only C5 succeeds, external consumers are the cause.
- If C4 OOMs quickly, demand on our side exceeded the cap. Report both, and do not raise the cap mid-study.

For a future paired attempt, set each arm's ceiling to ≥ 1.5× the observed C0 nominal time, and keep the stall watchdog.

## 4. Files

- `s009_forensics.py`: analysis, reconstruction, accounting, figures and optional `--run-dir` ingestion.
- `outputs/microbatch-table.csv`: 214 rows; time and memory are empty unless local logs are supplied.
- `outputs/analysis.json`: every derived number above.
- `figures/microbatch_lengths.png`, `memory_accounting.png`, `free_vs_step_time.png`, `time_budget.png`.

GB here means 10^9 bytes and MiB means 2^20 bytes. The 8,138 MiB post-run reading is taken from `studies/S009-value-comments/RESULTS.md`; its exact timing relative to process exit is not recorded.
