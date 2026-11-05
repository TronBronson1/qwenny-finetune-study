# Local 2048-token fit check — passed with explicit CPU input embedding

Date: 2026-11-03, America/New_York. User requested the fit check after reviewing
the assembled dataset. Corpus-level review sign-off is recorded against the exact
candidate-006 hash in ../dataset-v1/USER_REVIEW_2026-11-03.json. No separate
line-by-line human-review log or model-quality result is implied by that record.

## Result

The local RTX 3080 completed three synthetic 2048-token updates, adapter save,
fresh base/adapter reload and identical checked last-token logits. The working
configuration keeps the frozen input embedding table in ordinary CPU RAM and
copies lookup outputs back to CUDA. Transformer, output head and adapters remain
on the GPU. This explicit placement is different from relying on Windows to page
GPU allocations into shared memory. No app was closed, paused or reconfigured.

Base checkpoint/revision, native Windows packages, NF4/double quantization, BF16
compute, SDPA/PyTorch DeltaNet fallback, non-reentrant checkpointing, batch 1,
rank 4/alpha 8 and the 557056 query/value adapter parameters are unchanged from
the earlier experiments. The output head stays BF16 on CUDA. Only the frozen
input embedding changed placement.

Input embedding: model.language_model.embed_tokens; 1017118720 BF16 parameters,
2034237440 bytes (about 1.89 GiB) explicitly stored on CPU. The initial whole-model
load still happens on CUDA before this placement change. The original loading
device_map therefore does not describe final placement; report.json records the
manual CPU placement explicitly. Original checkpoint/model files were not modified.

Before and after moving the embedding, a four-token last-logit probe matched
exactly on both initial load and reload. The usual 64-token standard/chunked loss
comparison passed: loss difference about 6e-8 and gradient relative L2 difference
about 1.57%, under the predefined 3% tolerance. These are bounded checks, not a
claim of bit-identical gradients or exhaustive numerical equivalence.

## Measurements

Successful run: runs/trial-007-seq2048-chunk128-cpuembed-3steps.
Machine-readable summary: fit-2048-summary.json.

| Update | Seconds | Synthetic full-token loss |
|---|---:|---:|
| 1 | 4.312 | 0.0334913284 |
| 2 | 4.328 | 0.0334003419 |
| 3 | 4.500 | 0.0328017324 |

- All three had finite loss/adapter gradients, nonzero gradients, no base gradients
  and verified parameter changes.
- Adapter save and fresh reload passed; checked last-token logit difference 0.0.
- Training peak PyTorch allocation: 7655221760 bytes (about 7.13 GiB).
- Training peak PyTorch reservation: 8088715264 bytes (about 7.53 GiB).
- Minimum training-stage CUDA-reported free memory: 837885952 bytes (about 799 MiB).
- Minimum sampled nvidia-smi free memory: 1299 MiB.
- Nine valid Windows training-phase samples: process shared peak 85983232 bytes
  (82 MiB); dedicated peak 8354439168 bytes (about 7.78 GiB).
- Overall allocator peak including initial loading was 7940962816 bytes.
- Post-run nvidia-smi: 793 MiB used, 9261 MiB free. Trial process exited.

The APIs sample/account for different quantities and times under WDDM; their
values must not be combined into an exact accounting equation. Windows samples
approximately every 1.5 seconds and nvidia-smi samples also have overhead, so
short peaks can be missed. Three updates are a short capacity check, not proof
of hours-long stability, different adapter scope/rank, vision training or longer context.

## Baseline attempt retained

runs/trial-006-seq2048-chunk128-3steps used chunked loss with the input embedding
still on CUDA. Forward completed with CUDA free memory 0, but backward update 1
showed no recorded stage completion for over two minutes. Windows process shared
usage peaked at 656408576 bytes (626 MiB). Codex stopped only its owned trial to
avoid prolonged paging. No update completed; no backward/save/reload success or
CUDA OOM is claimed. termination.json overrides the unfinished started state in
its raw report. Both the raw report/logs and exact pre-change script are preserved.
Desktop occupancy varied between runs, so whole-GPU changes cannot be attributed
solely to the embedding placement. The intentional 1.89 GiB CPU weight placement
and lower allocator footprint are recorded separately.

## Reproduce and next step

From this directory:

    .\.venv\Scripts\python.exe trial.py --run runs/<new-name> --seq 2048 --loss-chunk 128 --steps 3 --windows-memory --cpu-embedding

Use a fresh output directory and check initial VRAM/RAM first. No cloud is selected.
The current dataset maximum is 1954 tokens under its provisional formatting
profile, so this test covers its measured sequence-length ceiling. It uses repeated
synthetic tokens and full-token loss, not the actual reviewed training records.
Actual assistant-only masking, exact reasoning/chat policy, nonzero target counts,
and matched base controls still need to be pinned/validated before task training.
The synthetic adapter is not a Qwenny quality candidate.

At the median 4.328-second 2048-token update, a hypothetical 60-example x 3-epoch
batch-one run padded to this length would take about 13 minutes of update compute
alone. Dynamic lengths, masking, accumulation and desktop activity can change that.
This is planning arithmetic rather than a full-dataset runtime measurement.
Evaluation and dataset export/pre-training checks are additional. Importing or
merging the eventual adapter into LM Studio/GGUF remains a separate compatibility test.
