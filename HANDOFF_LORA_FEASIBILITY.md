# Handoff: Qwenny LoRA feasibility experiment

## User objective and working arrangement

Continue the local Qwen experiment by determining a compatible LoRA training setup and measuring whether a small training trial fits this machine. LoRA remains the first planned alteration to model weights. The prompting comparison is complete; no adapter has been trained. Do not ask the user to find a compatible trainer or supply machine details that can be inspected locally.

Working directory:
`C:\Users\jalar\Desktop\Chat AI Lab\AI Labwork\Qwen\Fine Tuning Test`

Codex manages experiment files, evaluation and research. The user operates LM Studio and pastes Qwen outputs back into chat. Preserve this arrangement; do not automate LM Studio chats. Keep existing model files and experimental records intact. Files under the ChatGPT project's `sources/` are read-only synced references.

## Completed prompting comparison

Same intended system prompt/settings and matching seed 42; two new development task families, each tested with and without two fixed checked demonstrations. Each first response scored before exactly one repair. A = instructions only; B = instructions plus demonstrations.

| Task | A first | A after one repair | B first | B after one repair |
| --- | --- | --- | --- | --- |
| T01 rotation | Fail collection | Fail: 32 passed, 3 failed | Fail collection | Fail collection |
| T02 clock parsing | Fail strict coverage | Pass | Fail strict coverage | Fail strict coverage |

First-attempt strict acceptance: A 0/2, B 0/2. After at most one repair: A 1/2, B 0/2. Both clock first attempts and repairs passed their references and detected all five fixed mutants. Initial clock suites omitted exact built-in int output assertions. A's repair used `type(result) is int` and passed; B's repair used `isinstance(result, int)`, which accepts subclasses, and remained incomplete.

No accuracy benefit from these demonstrations was observed in this small development check. Do not generalize that demonstrations harm accuracy or claim a training effect. Two task families, one intended seed, and user-operated settings/input capture limit inference. No timings/tokens recorded. References/mutants are authored and agent-checked; independent human review remains pending. These visible families cannot be reused as unseen final tests.

Results: `prompt-comparison/COMPARISON_RESULTS.md`. Full saved answers, intended prompts, per-attempt reports and execution logs: `runs/comparison-T01-A`, `runs/comparison-T01-B`, `runs/comparison-T02-A`, `runs/comparison-T02-B`.

## Checked examples and evaluator

Two original demonstrations: integer batch counts and literal prefix removal. Each target passes 23 reference tests and detects five designated mutants. Additional bounded independent oracle calculations passed 3,720 valid-input checks (same author, not independent reviewer). Explicit argument tuples, separate exception tests and finite coverage limitations are included.

Files: `prompt-comparison/DEMONSTRATIONS.md`, `demonstrations/`, `CHECK_RESULTS.json`, `ORACLE_RESULTS.json`. They are training candidates awaiting second-person review, not a sufficient training dataset. Do not train on unreviewed failed Qwen outputs. Initial source hashes exist in `SHA256.json`; later evaluation/handoff additions are not necessarily represented there.

Executable evaluator: `prompt-comparison/evaluate.py`. Python used for checks: `C:\Users\jalar\AppData\Local\Python\pythoncore-3.15-64\python.exe`, pytest 9.2.0. Default python/py WindowsApps aliases failed to launch; use explicit installed paths.

## Machine and model facts

- Windows / PowerShell; RTX 3080 with 10,240 MiB VRAM; NVIDIA driver 610.74.
- Approximately 32 GB system RAM. Prior CPU record: i7-11700KF, not reverified.
- Latest read-only snapshot: 1,553 MiB GPU memory free while inference/desktop workloads were resident. This is occupancy, not proof of training fit. Do not terminate apps without coordination.
- WSL reports not installed.
- Python 3.12.10: `C:\Users\jalar\AppData\Local\Python\pythoncore-3.12-64\python.exe`. Its pip inventory contained only pip 25.0.1; other environments may exist.
- Free storage snapshot: C about 254.1 GiB; D about 1862.8 GiB. Recheck before downloads.
- Active inference: LM Studio 0.4.28, display identifier `qwen/qwen3.5-9b`, GGUF Q4_K_M. Exact LM Studio file/source/hash and engine revision remain unresolved.
- Separate Ollama installation contains qwen3.5:9b and 2b; its model/blob IDs in `02_MACHINE_AND_TRAINING.md` identify Ollama artifacts only. Do not assign them to LM Studio or assume an exact upstream checkpoint match.
- `C:\Users\jalar\.lmstudio\models` exists and contains `lmstudio-community`. The earlier search for `*9b*.gguf` there found no file; resolve actual model location through relevant nonsecret model metadata or ask a focused question if needed. Do not read credential files.
- Local LM Studio API at localhost:1234 refused connection. No server was started or settings changed.

## Preserve current inference controls

See `04_LM_STUDIO_BASELINE.md` for full recorded settings and `prompt-comparison/SYSTEM_PROMPT.txt` for the fixed current prompt (candidate v1 from `05_FIRST_ALTERATION.md`, not the earlier blank prompt).

Thinking on; unrestricted reasoning/no explicit output cap; temperature 1; top_k 20; top_p 0.95; presence penalty 1.5; seed 42; test context setting 16134 (loaded counter displayed 16384); GPU offload 32; thread pool 6; evaluation/physical batch 2048/512; Flash Attention on. Do not silently substitute training configuration for these inference settings. A short training sequence is a distinct feasibility setting, not a change to the historical baseline.

## Next experiment: compatibility and measured memory fit

1. Resolve exact model identity/source and architecture. Find/pin an upstream trainable checkpoint, tokenizer/processor and chat template. A local GGUF inference file is not automatically the right training checkpoint.
2. Research current primary documentation for trainer support of this exact Qwen3.5 architecture, RTX 3080 and Windows or WSL. Verify package/version support rather than copying a recipe for older Qwen. Explain one concrete recommended setup and relevant tradeoffs. No trainer is selected or verified yet.
3. Inspect existing environments, packages and storage as needed; prepare an isolated, reproducible setup. Explain concrete user actions if OS installation/restart is needed. Do useful research/preparation before asking the user to act; avoid vague permission questions.
4. Before a full run, trial a short sequence, batch size 1 and small LoRA scope/rank with supported memory-saving options. Quantized-base LoRA may be a candidate, not a verified fit. Record base revision, packages, trainable module selection and configuration.
5. Measure a real forward/backward/optimizer step and adapter save/reload: peak VRAM, memory headroom, gradients only on intended adapter parameters, finite loss and successful reload. Loading a model or running inference alone does not establish training feasibility. Record failures honestly.
6. After feasibility, assemble enough reviewed training/development/regression data before a meaningful adapter experiment. Repeat matched base A/B controls in the eventual training/evaluation runtime before attributing changes to LoRA. Export/merge/requantization and return to LM Studio/Ollama require separate compatibility checks; do not promise them yet.

If 9B cannot fit, report the measured limitation and consider supported memory reductions. Switching to 2B creates a separate experiment and requires new matched baselines; do not silently switch models.

## Main reference files

- `README.md` — overview (older status paragraphs exist; latest completed comparison supersedes them).
- `01_EXPERIMENT_PLAN.md` — arm definitions, scoring and future adapter comparison.
- `02_MACHINE_AND_TRAINING.md` — inventory and feasibility checklist, with latest user-input clarification.
- `03_DATASET_RULES.md` — family splits, review and leakage rules.
- `04_LM_STUDIO_BASELINE.md` — inference settings.
- `06_DEMONSTRATION_COMPARISON.md` and `prompt-comparison/COMPARISON_RESULTS.md` — completed prompting experiment; latest results supersede earlier pending status.

The next chat should begin with model/environment inspection and current compatibility research, then produce a concrete feasibility plan. The user needs help doing this, not another instruction to research it themselves.
