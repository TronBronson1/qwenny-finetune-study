# LM Studio pilot configuration

Recorded November 3, 2026 from user-supplied screenshots. This is the active pilot configuration; earlier Ollama inventory describes a separate installation and does not identify this model file or its runtime settings.

The user reports that approximately 16K context has been needed for their thinking-mode, multiple-instruction workflow. Retain this working configuration for the pilot. This is an observation about that workflow, not a universal minimum for thinking mode.

## Loading settings shown

| Setting | Screenshot observation |
| --- | --- |
| Application | LM Studio 0.4.28 |
| Model display name | Qwen3.5 9B |
| Loaded identifier | qwen/qwen3.5-9b |
| Format / quantization | GGUF / Q4_K_M |
| Context entered before loading | 16134 |
| Context counter after loading | Screenshot shows 0/16384; user subsequently confirmed 16134 is the test setting. Use 16134 in run records; counter discrepancy retained as an observation. |
| GPU offload | 32 |
| CPU thread pool size | 6 |
| Evaluation / physical batch size | 2048 / 512 |
| Max concurrent predictions | 4; run pilot requests one at a time |
| Unified KV cache | On |
| Context checkpoints | 32 |
| Reasoning budget message | Blank |
| RoPE frequency base / scale | Auto; overrides unchecked |
| KV cache GPU offload | On |
| Keep model in memory | On |
| Try mmap | On |
| On-demand tensor loading | Auto |
| Seed | Enabled, 42 |
| Speculative decoding | Off |
| Flash attention | On |
| K/V cache quantization overrides | Unchecked; actual cache types not established |
| llama.cpp arguments override | Off |
| Remember model settings | Checked |
| Estimated GPU memory | 7.51 GB; estimate only, not measured peak usage |

## Inference settings shown after loading

| Setting | Screenshot observation |
| --- | --- |
| Enable thinking | On |
| Reasoning budget | Unrestricted; limit unchecked |
| Temperature | 1 |
| Limit response length | Unchecked; no explicit user cap |
| Context overflow policy | Truncate Middle |
| Stop strings | Empty |
| Top K | 20 |
| Repeat penalty | Unchecked |
| Presence penalty | Enabled, 1.5 |
| Top P | Enabled, 0.95 |
| Min P | Unchecked |
| Structured output | Off |
| Preset | Unsaved Preset |
| System prompt | User subsequently confirmed blank for the earlier pilot. A later run used the candidate prompt in 05_FIRST_ALTERATION.md; see runs/pilot-002-system-prompt. |

Do not substitute the earlier proposed temperature 0.2, presence penalty 0, thinking off, 8192 context, or output cap 4096 for these observed pilot settings. Keep sampling controls as shown.

Save the inference preset as `Qwenny Coding Pilot v1` without changing its values. The screenshots remain the evidence for load settings. Start each task in a fresh chat; save exact prompts, complete responses, actual timing, and any overflow/cutoff. If truncation removes part of the request, record the run as compromised rather than treating it as a clean task score. Unrestricted reasoning/response limits still operate within runtime and context constraints.

User confirmed 16134 as the test context setting. Before formal evaluation, confirm exact GGUF filename/source/hash, engine version, and system prompt. These identity details are not established by the friendly model label. No model evaluation has been performed by recording these settings.

## Screenshot references

Original files in C:\Users\jalar\Pictures\Screenshots:

- Screenshot 2026-11-03 140812.png — upper loading controls, context 16134.
- Screenshot 2026-11-03 140819.png — middle loading controls, seed 42.
- Screenshot 2026-11-03 140826.png — lower loading controls.
- Screenshot 2026-11-03 141048.png — loaded chat, thinking, temperature, length and overflow controls.
- Screenshot 2026-11-03 141135.png — sampling settings and loaded context counter.
