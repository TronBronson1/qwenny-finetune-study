# Publication notes

This repository is a curated snapshot of the local working folder, taken on **November 4, 2026**. Apart from the additions listed at the end, file contents are byte-identical to the originals (see `.gitattributes`), so the SHA-256 manifests inside the project still verify the files that are included.

## Deliberately not published

| Excluded | Why |
|---|---|
| **Final (`EV###`) and regression (`RG###`) tasks**: their specs, references, mutants, gold suites, request packets (`final-requests.jsonl`, `regression-requests.jsonl`), builder sources (`tasks_final.py`, `tasks_regression.py`) and validation runs | They are the sealed held-out benchmark. Publishing them would contaminate the final evaluation, and possibly future models' training data. |
| Files that list held-out task names or signatures: `family_plan.json`, candidate `manifest.json`, `INDEX.md`, `approvals.template.json`, validation `summary.json`, `assembly-*.log`, `dataset-v1/preflight.log` | Same reason: even task names and parameter lists reveal the held-out topics. |
| Base model weights, LoRA adapters, optimizer and RNG states (`*.safetensors`, `*.pt`, …), and the `checkpoint/`, `runs/`, `candidates/` folders | Too large for git, and not needed to follow the research. The base model is public on Hugging Face at the pinned revision. |
| Tokenized training caches (`prepared-*`) | Derived data, re-creatable from the training tasks and scripts. |
| Python environments, Hugging Face caches, `__pycache__` | Machine-specific. |

Because of these exclusions, some hash manifests (for example `dataset-v1/candidate-006/SHA256.json`) list files that are absent here. That is intentional: the hashes of held-out files are kept as a public record that the held-out set existed, unchanged, before any final evaluation.

## Other notes

- Logs and JSON records contain the original local Windows paths. They were left as-is so the recorded hashes and evidence stay exact.
- Older documents describe the project's status at the time they were written. [START_HERE.md](START_HERE.md) and [program/CURRENT_STATE.md](program/CURRENT_STATE.md) give the current status.
- Before publication, an automated scan checked every included text file for held-out task names, held-out spec lines, API tokens, private keys and personal email addresses.

## Added for publication

`README.md` (portfolio overview), `PUBLICATION_NOTES.md`, `.gitignore` and `.gitattributes`. The project's original introduction was renamed from `README.md` to [README_ORIGINAL.md](README_ORIGINAL.md); nothing linked to the old path.
