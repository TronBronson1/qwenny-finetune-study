# S009 — stopped at the training-arm time ceiling

Ended November 4, 2026 (America/New_York). **No paired model-quality result was obtained.** The frozen controller stopped the first training arm at 1,200 seconds. It did not start the comment training arm or any scored task generation. No endpoint, winner or deployment was selected.

## Completed preparation

- Verified 22 handoff sources and all 1,280 candidate-007 manifest entries; preserved parent snapshots, old results and reserved splits.
- Materialized two exact-hash 60-record exports with per-record provenance and the certified TR058 fit overlay. Current user delegation is recorded separately from historical candidate-006 approval.
- Added 23 oracle/reference-verified calculation comments across TR007/TR010/TR038/TR049. Treatment executable AST is unchanged. TR049 optional comma spacing is removed in both arms.
- Exact supervised decoding passes for every training and development loss row. Prompt/roles/empty thinking wrapper are masked; no truncation. The 12-task development A/B no-gradient interface remains 24 rows, never optimizer data.
- Maximum baseline/comment chat length: 1,880/1,920. Per-pass input totals: 61,313/61,677; supervised totals: 42,255/42,619. The intended treatment adds 364 supervised tokens per pass, not equal token exposure/FLOPs.
- Both training packets pass 120 reference suites and 664 designated mutant executions. TR058 uses the previously certified complete per-case outcome-vector binding because its display IDs differ. Its interim engine log says FAILED before the final vector check; final validation has zero failures.
- The input-tracing model-suite scorer passes all eight renamed gold suites and all 52 selected designated fixtures, plus six negative controls. Final generated-source/requirement/witness review remains required; no arbitrary model suite was accepted by an automated semantic verifier.
- Missing approval, wrong hash, changed token files and legacy prepared-corpus selection are rejected.

## GPU gates and actual training

Both separate preflights passed the actual longest-example forward/backward, frozen-base gradient exclusion, masked standard/chunked loss comparison and cached generation smoke. Both initial adapter SHA256 values equal `ccbcec6aa257f813a89d8a0a269bbc2125a3312ba63231bf009af67420a6e80d`. Standard/chunked loss matched numerically; gradient relative L2 difference was 0.0128726, below the frozen 0.03 tolerance. Both smoke outputs were `blue` followed by im_end.

| Stage | Actual outcome |
|---|---|
| Baseline preflight | Passed; 179.22 seconds |
| Comment preflight | Passed; 245.00 seconds |
| Fresh baseline optimizer trajectory | Stopped at 1,200-second arm ceiling; 213 completed logged microbatches, 53 logged updates |
| Baseline checkpoints | E1 and E3 saved with optimizer/RNG and saved probes; no E5; fresh imports not attempted |
| Fresh comment optimizer trajectory | Not started |
| Matched base / baseline E5 / comment E5 attempts | All 24 unattempted |
| Primary/strict/requirement/mutant/prose model outcomes | Not measured |

The baseline last child report still says `training`: forced termination occurred before the child could rewrite it. The terminal controller record and `TERMINATED_BY_CONTROLLER.json` are authoritative. Reported completion/update counts come from finished log entries; no claim is made about unlogged work in the interrupted batch. The retained E1/E3 checkpoints cannot replace the prospectively chosen E5 endpoint.

Total GPU orchestration wall time, including file verification/loading and both preflights, was 1,624.30 seconds (27.07 minutes). The completed baseline microbatches account for 217,219 input and 149,563 supervised tokens. Microbatch timing totals omit the unfinished final batch and preparation/evaluation/loading.

## Observed slowdown and limits

Median completed batch time was 2.672 seconds among 209 positive-CUDA-free-memory samples and 34.352 seconds among four zero-free-memory samples. The next batch remained unfinished until the controller timeout. Training-phase peak allocated/reserved GPU memory was 7,531,739,136 / 8,120,172,544 bytes. These are allocator measurements; driver samples are also retained.

The timing shift coincides with reported CUDA-free memory reaching zero. It does **not** identify the competing resource/process, establish a causal mechanism or prove shared-memory spill. Windows per-process memory sampling again produced zero usable rows. After termination, a driver query reported 8,138 MiB free; that single post-run observation is below the existing 8 GiB fresh-load guard. No further load was attempted, and no app was closed.

No nonfinite loss or intended-gradient check failure was logged before the interruption. This is a budget stop with observed runtime instability, not a demonstrated model-quality failure or a proved out-of-memory exception.

## Freeze/provenance qualifications

The protocol, packets, scorer, tasks, inference settings, endpoints and controller were frozen before GPU work. A secondary requirement-key/denominator catalog was explicitly recorded after training startup but before any scored task answers; its timing and hash are in measurement-supplement-binding.json. It operationalizes the frozen contract measure; it must not be described as a catalog frozen before training.

The exact executed packet-builder source is archived under its recorded original hash. The later frozen builder only moves two imports into main so scoring Python can import pure helpers; non-import AST is identical. See builder-source-binding.json. Archived candidate files and the original freeze were not rewritten.

Calibration/semantic review is same-agent and finite, informed by external parent review. No independent acceptance of all revised tasks is claimed. All development loss exposure and prior visible-task generation exposure remain disclosed. No final/regression contents were accessed, and no working model or LM Studio configuration was changed. Process-scoped keep-awake ended with the terminated/completed processes; no persistent power settings changed.

## Decision

End S009 as an incomplete controlled comparison. Preserve every artifact; no retry, cap extension, partial-checkpoint substitution, fresh import or model generation was launched after the stop. This study supplies reusable preparation/scoring/preflight evidence and a runtime diagnostic, but cannot tell whether comments improve Qwenny. Before a separately frozen attempt, diagnose and demonstrate stable sustained local resource availability and realistic wall-time headroom. Retain the calibrated packets and scoring rules; do not tune targets from development failures or choose E1/E3 because E5 was not reached.

[Protocol](PROTOCOL.md) · [Stopped evidence](stopped-evidence-001.json) · [Controller](execution-001.json) · [Next handoff](HANDOFF.md) · [Observer Report 006](../../observer/REPORT_006.md)
