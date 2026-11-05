# Qwenny LoRA compatibility and memory-fit investigation

Date: 2026-11-03. This directory is additive; prior comparisons and models are preserved.

**Latest:** setup and downloads completed; two actual training/save/reload trials
passed with marginal memory headroom. See `RESULTS.md` and `STATUS.md`. The
preparation narrative below records the investigation; its earlier download-status
paragraphs are superseded by those completed results.

## Identity and inspection

LM Studio file: `C:\Users\jalar\.lmstudio\models\lmstudio-community\Qwen3.5-9B-GGUF\Qwen3.5-9B-Q4_K_M.gguf`.
Size from download record: 5,627,044,256 bytes. Locally computed SHA-256:
`cd76ec205963b3b33350093e6904d9de16c4e666fd104e1f632d25c7f15f2a13`.
This matches LM Studio's recorded download hash. Recorded source is
`lmstudio-community/Qwen3.5-9B-GGUF`, file `Qwen3.5-9B-Q4_K_M.gguf`.
Cached GGUF metadata: architecture `qwen35`, 32 layers, nominal maximum context 262144.
Historical test context remains as recorded in the handoff; this maximum is not a test setting.
The upstream revision used by the GGUF conversion and LM Studio engine revision remain unresolved.

Training candidate: `Qwen/Qwen3.5-9B` at
`c202236235762e1c871ad0ccb60c8ee5ba337b9a` (public Hugging Face API resolved today).
Tokenizer, processor configuration, and chat template must come from this same revision.
Pinned upstream metadata is saved in `upstream-metadata/`; the weight index reports
19,306,216,416 bytes of tensors. Full weights are separate from the GGUF.
No assertion of exact conversion lineage is made. Repeat base controls in the training runtime later.

The upstream config declares `Qwen3_5ForConditionalGeneration`, dense 32-layer text
backbone, three linear-attention blocks per full-attention block, untied embeddings,
248320 vocabulary, hidden size 4096, and a vision encoder. This is not an older Qwen3 model.

Machine recheck: RTX 3080, 10240 MiB, driver 610.74. Initially 8497 MiB occupied;
later 1492 MiB occupied / 8562 MiB free. Occupancy changes are not training measurements.
WSL is not installed. C free approximately 254 GiB, D approximately 1863 GiB.
Python 3.12.10 initially had only pip 25.0.1. Python 3.15 is reserved for prior evaluation;
new packages go only into this directory's `.venv`. CIM RAM inspection was denied;
the prior approximately 32 GB record remains unverified today.

## Selected first setup

Native Windows Python 3.12, PyTorch 2.14.1 CUDA 12.6 wheel, Transformers 5.22.1,
PEFT 0.21.2, Accelerate 1.15.0, bitsandbytes 0.50.2. These are selected candidate
versions, not a claim that the entire combination has passed a training step.
Exact transitive versions are frozen after installation. The CUDA version reported
by nvidia-smi describes driver capability; it is not the installed PyTorch runtime.

Use the official Transformers architecture and its PyTorch DeltaNet fallback with
SDPA for full attention. This avoids requiring Windows builds of optional
causal-conv1d/FLA kernels or an OS change. The fallback can be slower and more memory
hungry. NF4 with double quantization, BF16 compute, frozen base, gradient checkpointing,
and a tiny adapter are the first memory probe. There is no CPU/disk dispatch and no
automatic switch to 2B. A failed native fallback does not rule out optimized Linux kernels.

Unsloth is a concrete second candidate, not installed in the same environment. Its
Qwen3.5-specific guide supports this family and requires Transformers v5. Its BF16
9B memory estimate exceeds this GPU, and its current guide cautions against 4-bit
Qwen3.5 tuning. Accordingly this NF4 probe establishes plumbing/memory only; quality
needs separate matched controls. The guide also contains a dense-27B 4-bit example
comment that is less restrictive than its warning; we use the conservative warning.
Unsloth documents native Windows, Conda and WSL routes. If the native fallback fails,
investigate an isolated Unsloth Core environment before requiring WSL. Do not install
WSL, reboot, terminate apps, or change LM Studio settings automatically.

## Trial contract

`trial.py --run runs/<new-name> --seq 128` requires a fresh output directory.
Batch 1, rank 4 / alpha 8, dropout 0, AdamW learning rate 1e-4, one update.
Adapters target exactly 16 q_proj/v_proj modules in eight full-attention blocks.
An assertion stops the run if the architecture differs. Vision, MLP, embeddings,
and DeltaNet weights remain frozen. Standard prepare_model_for_kbit_training
upcasts unquantized weights. The trial explicitly restores only frozen input
embeddings and the output head to BF16 after preparation, uses BF16 autocast, and
records this policy. To avoid the transient upcast itself, preparation implements
PEFT's freezing and non-reentrant checkpointing protocol selectively: all other
nonquantized FP16/BF16 parameters are upcast, while those two frozen matrices stay
BF16 throughout. Reload uses the same policy.

Synthetic repeated chat-template tokens test machinery only, with full-token loss.
This is not task SFT, assistant-only masking, reviewed training data, or an accuracy
experiment. Never deploy the resulting disposable adapter as Qwenny.

Required evidence: full CUDA base load, finite forward loss, finite nonzero adapter
gradients with no base gradients, an actual optimizer update, safe adapter save,
base release, fresh base/adapter reload, and agreeing last-token logits.
Record PyTorch allocated/reserved peaks at each stage, plus sampled whole-GPU
memory every approximately 0.5 seconds. Samples can miss brief peaks; PyTorch
allocator counters exclude allocations outside its allocator. Report both rather
than claiming an exact whole-device transient maximum. Compile and load peaks count.
The run refuses to load with less than 8 GiB initially free. This is a protective
entry condition, not a guaranteed fit. Keep at least about 0.5 GiB observed headroom
for a practical desktop trial; a successful but nearly full run is marginal.

If it OOMs, retain traceback, stage and memory logs. A 64-token repeat is a separate
run; no silent config changes. If embeddings dominate, investigate supported text-only
loading or quantization exclusions carefully before another run. A different loader
or quantization policy must be recorded as a separate configuration.

## Primary sources checked

- https://huggingface.co/Qwen/Qwen3.5-9B (official checkpoint)
- https://huggingface.co/Qwen/Qwen3.5-9B/raw/main/config.json (config; pinned local copy saved)
- https://huggingface.co/docs/transformers/model_doc/qwen3_5 (architecture and optional fast kernels/fallback)
- https://huggingface.co/docs/peft/developer_guides/quantization (k-bit preparation and LoRA)
- https://huggingface.co/docs/transformers/quantization/bitsandbytes (Windows/CUDA support and NF4)
- https://huggingface.co/docs/bitsandbytes/installation (Windows wheels, hardware requirements)
- https://pytorch.org/get-started/previous-versions/ (2.14.1 CUDA 12.6 Windows wheel)
- https://unsloth.ai/docs/models/qwen3.5/fine-tune (exact family support and memory/quantization guidance)
- https://unsloth.ai/docs/get-started/install/windows-installation (native and WSL installation routes)

## Experiment boundary

No performance claim follows from this trial. Existing two demonstrations still
await second-person review; failed Qwen outputs are excluded from training. After
feasibility, assemble reviewed training/development/regression data and new unseen
final families. Match base controls in the eventual training/evaluation runtime.
LM Studio import, merge and GGUF export are separate checks and are not promised.

## Installation evidence and download status

Installed the selected versions into `.venv`. `dependency-check.txt` reports no
broken requirements. `imports-preflight.txt` confirms the exact Qwen3.5 class,
PEFT and bitsandbytes imports. `cuda-preflight.txt` confirms PyTorch 2.14.1+cu126,
CUDA runtime 12.6, RTX 3080 and BF16 support. RAM rechecked using psutil:
34,185,228,288 bytes total, 20,830,867,456 bytes available at inspection.
`packages.lock.txt` records resolved transitive packages.

Hugging Face Hub accelerated download stalled; its standard HTTP retry also
stalled before transferring the large weights. Both owned downloader processes
were stopped, and their logs retained. `download_direct.py` uses public HTTPS,
an immutable revision, resumable partial files and LFS SHA256 validation instead.
It writes only `checkpoint/<revision>/`. The trial loads that local directory
with `local_files_only=True`. No credentials or remote model code are needed.

Reproduce from this directory with PowerShell:

```powershell
.\setup.ps1
.\.venv\Scripts\python.exe download_direct.py
.\.venv\Scripts\python.exe trial.py --run runs/trial-001 --seq 128
```

Do not run multiple downloaders/trials concurrently. The original `download.py`
is retained as the unsuccessful Hub-client route; use `download_direct.py`.
No model fit conclusion is justified until a completed trial report exists.
