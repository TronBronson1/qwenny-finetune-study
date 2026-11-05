# Machine inventory and training feasibility

## What the user needs to provide

No additional hardware specification or LoRA package selection is required from the user at this stage. Codex can inspect the local machine and model records, research current training software support, and prepare a specific setup. LoRA is the adaptation method; the compatibility question is which training software supports the exact Qwen architecture, GPU and operating system. A compatible setup must then be tested for actual memory use.

Follow-up read-only inspection confirmed RTX 3080 with 10,240 MiB VRAM and driver 610.74. At that instant only 1,553 MiB VRAM was free; this is current occupancy, not a training memory-fit result. WSL reports not installed. The inspected Python 3.12 environment lists only pip 25.0.1, with no training packages; this does not rule out other environments. Free storage was approximately 254.1 GiB on C and 1862.8 GiB on D. No installations or training steps performed.

Codex's next investigation: resolve the LM Studio model file/source; check current trainer support for that exact architecture and RTX 3080; propose a pinned isolated training environment; then measure a small adapter training/save/reload trial. User involvement is only needed for an inaccessible model location or a concrete setup decision such as an OS-component installation. Do not ask the user to discover a compatible trainer on their own.

Update: the user is conducting the pilot in LM Studio, not Ollama. See `04_LM_STUDIO_BASELINE.md` for the active settings. Ollama identifiers and blob hashes below identify only the separate Ollama installation; they must not be assigned to the LM Studio GGUF without verification.

Inspected November 3, 2026 using local read-only commands. No downloads, installations, training, or model changes performed.

| Item | Observation |
| --- | --- |
| Platform | Windows; PowerShell |
| GPU | NVIDIA GeForce RTX 3080 |
| GPU memory | 10,240 MiB, confirmed by nvidia-smi |
| NVIDIA driver | 610.74 |
| System memory | 34,185,228,288 bytes reported by Windows, approximately 31.84 GiB; nominal 32 GB |
| Ollama client | 0.40.13; server version not yet captured |
| Primary installed model | qwen3.5:9b |
| Ollama listed ID | 56671c2ab938 |
| Architecture/size | qwen35, 9.0B |
| Quantization | Q4_K_M |
| Installed artifact format | GGUF, confirmed by local manifest |
| Model blob SHA-256 | 02d45dc1cf451ba2475ac33b301c2dd8f985abe4c182ce04a1f2f5bf0260278d |
| Model blob bytes | 5,629,109,120 |
| Vision projector | Separate 921,704,832-byte blob; text-only task planned |
| Installed alternate | qwen3.5:2b, ID 0689d44085e0; not selected for the primary comparison |
| Python | Python 3.12.10 executable verified at C:\Users\jalar\AppData\Local\Python\pythoncore-3.12-64\python.exe |

Ollama reports a model context capacity of 262144; this is not a recommended context allocation for this GPU. Existing defaults include thinking on, temperature 1, presence_penalty 1.5, top_k 20, top_p 0.95. The experiment deliberately overrides these and must record the effective request.

The prior notes record an i7-11700KF; CPU identity was not reverified here. PyTorch/CUDA training support, WSL availability, free disk space, compatible package versions, and exact upstream weight revision remain unverified.

## What the inventory establishes

We have identified the installed inference model and available memory. It does not establish that a 9B training job fits. Even a frozen quantized base shares memory with adapters, activations, gradients, optimizer state, runtime buffers, and the display workload.

Candidate upstream identity: [Qwen/Qwen3.5-9B official model card](https://huggingface.co/Qwen/Qwen3.5-9B). This is a candidate training source, not proof that its current revision exactly matches the local GGUF. Pin and reconcile the upstream revision and tokenizer before training. The model card describes multimodal loading; generic text-only training snippets for older Qwen architectures must not be assumed compatible.

## Candidate path, pending compatibility checks

Investigate quantized-base LoRA using a stack that explicitly supports Qwen3.5, this GPU, and the selected Windows or WSL environment. [PEFT's quantization guide](https://huggingface.co/docs/peft/en/developer_guides/quantization) describes adapter training with a quantized base. Its examples are not a validated recipe for this machine/model. The installed Q4_K_M GGUF is not automatically a training checkpoint for that workflow.

Before a full run:

1. Pin exact model revision, processor/tokenizer, chat template, training packages, and data hashes. Verify architecture support and intended trainable modules rather than copying another model's layer names.
2. Run base inference on one reviewed example in the training runtime; compare the prompt rendering with the planned evaluation request.
3. Trial a short sequence, batch size 1, low-rank adapter and gradient checkpointing if supported. Treat rank and sequence length as development choices, not established hardware settings.
4. Measure peak VRAM through a forward/backward/optimizer step and adapter save/reload. Verify only intended adapter parameters receive gradients and that a saved adapter reloads successfully.
5. Check the full evaluation context also fits. Freeze settings only after a successful trial with recorded memory headroom.

If 9B does not fit, reduce sequence length or adapter scope, or investigate another supported memory-saving method. The installed 2B model offers a separate educational fallback; restarting A/B/C on 2B creates a new experiment, not evidence about adapting 9B.

## Returning to Ollama

Export/import compatibility remains untested. [Ollama's import documentation](https://docs.ollama.com/import) describes Safetensors and GGUF imports; it does not establish that this exact adapter/architecture path will work. First evaluate adapter effects in the training runtime. Treat conversion, merging, and requantization as a subsequent deployment experiment with matched base controls.

## Remaining capture

Save Ollama server version, complete effective template/configuration, full model manifest, upstream revision mapping, free disk space, and training package inventory before a baseline is frozen. Preserve original models; use a new adapter/output directory for each run.
