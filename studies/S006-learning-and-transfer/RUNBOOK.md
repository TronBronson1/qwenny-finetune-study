# S006 reproduction and evidence map
Run ID: s006-001. Local Windows / RTX3080; no training updates.

## Files
- PROTOCOL.md: historical draft; PROTOCOL_FROZEN.md: actual execution specification.
- selection.json and inputs/: deterministic metadata selection, exact messages, rendered prompts and input token IDs.
- COVERAGE_RUBRIC.json: acceptance review categories declared before generation.
- REVIEW.md: pre-execution self-review and its limits.
- preflight.json and preflight/: selected authored gold suites checked against correct and three defective implementations, using Python3.15/pytest9.2.
- freeze-manifest.json: SHA256 fingerprints recorded before generation.
- ../../training-v1/probes/s006-001/: generation report, raw answers, token IDs, progress, prompt copies, model reload checks and GPU/process memory logs.
- ../../training-v1/s006-001.log: generation process output.
- ../../training-v1/scoring/s006-001/: definitive scoring output, created after source inspection.

The completed report is RESULTS.md, with INTERPRETATION.md and EXECUTION_REVIEW.md. Post-run helpers training-v1/audit_s006.py and training-v1/finalize_s006.py verify provenance and combine frozen execution with manual coverage review; they do not generate new attempts. Their final fingerprints are in result-sha256.json.

## Reproduction procedure
Use the pinned local checkpoint and package environment documented in the frozen inputs; do not assume an existing GGUF has the same lineage. Compare actual dependencies/hardware before claiming identical reproduction. The manifest records local original paths relative to the experiment root.

Preparation used training-v1/prepare_s006.py with the existing lora-feasibility/.venv/Scripts/python.exe. It only selected training/development metadata and rendered inputs. Pre-generation preparation encountered a development-ID suffix mismatch and an existing partial-input directory; these were corrected before selection/freeze, without any model answers. The final preparation source is frozen.

CPU preflight used the installed Python3.15 executable and training-v1/preflight_s006.py; all 32 runs passed their expected reference/mutant outcomes. It then created the freeze manifest. Generation used the model environment and training-v1/s006_probe.py with stdout/stderr saved to training-v1/s006-001.log.

The scripts deliberately refuse to overwrite existing selection/freeze/run output. To repeat the study, make a separately identified run and protocol amendment with fresh destinations; retain s006-001 unchanged. Do not delete or overwrite output to make a rerun look like a first attempt.

After generation, inspect every candidate source, bind review to its SHA256, then run training-v1/score_s006.py with explicit --probe, --reviews, --out and --python arguments. This scorer runs in Python3.15 without importing the GPU runtime. Complete a separate contract/prose review using the frozen rubric before assigning strict acceptance. A full operating-system security sandbox is not claimed by directory/process isolation.

## Resource and integrity notes
The model process makes a temporary keep-awake request and releases it on normal exit/finally cleanup; it changes no persistent power plan. No other apps should be closed automatically. GPU-wide monitoring and per-process Windows monitoring are attempted; missing samples must be reported rather than inferred. Timeouts are soft token-boundary limits. Preserve aborted/partial cells and distinguish infrastructure failure from model quality.
