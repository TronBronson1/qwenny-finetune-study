# Handoff — next controlled training study

Prepared November 4, 2026 (America/New_York). Work root: this directory.
**Next study: S009, value-comments training ablation. Design/preparation pending; no new training has started.**

## Read first

1. [Current program state](program/CURRENT_STATE.md).
2. [Next training study brief](program/NEXT_TRAINING_STUDY.md).
3. [Observer Report 005](observer/REPORT_005.md).
4. [S007 calibration results](studies/S007-measurement-repair/RESULTS.md), [certificate](studies/S007-measurement-repair/calibration-certificate.json), and [fit overlay](studies/S007-measurement-repair/TRAINING_FIT_OVERLAY.json).
5. [S008 results](studies/S008-fixed-input-values/RESULTS.md) and [interpretation](studies/S008-fixed-input-values/INTERPRETATION.md).
6. [Machine handoff and source fingerprints](program/handoffs/controlled-training-001.json).

Do not start from an older HANDOFF file's next-step recommendation. NEXT_TRAINING_STUDY.md is a proposal archived in the S008 result fingerprints, not an execution protocol; copy/finalize it under a new S009 directory rather than rewriting that archived artifact.

## Purpose and current conclusion

The user wants a worthwhile, understandable proof-of-concept study of improving Qwenny on ordinary local hardware. Provide a separate plain-language observer report and glossary updates after each study. The user delegates routine design, implementation, testing and documentation; do not ask them to manage technical details.

Local adapter training/import feasibility is established. Reliable practical improvement over a strong prompted base has not been established. No candidate selected or deployed.

Adversarial review found gold/rubric mismatches. Original S006 strict zero is a historical rubric outcome, not a calibrated standalone capability measure. Preserve it; do not retroactively award E5/DV008 a first success.

## What is complete

**S007:** candidate-007 is a separate training/development-only repair: 60 training and 12 development tasks. All 72 correct references are byte-identical to parent candidate-006. Revised gold passes 1,475 reference cases and rejects all 407 designated mutants at concrete declared witnesses. Five negative controls are rejected. Builder performed 10,037 valid-domain reference/oracle comparisons.

There are 216 legacy mutants and 191 additional requirement fixtures. These are correlated finite checks, not independent task samples or exhaustive coverage. Eight remaining keyword flags are false positives explained in STRUCTURAL_REVIEW.md. Three shape-priority notices were semantically reviewed. New candidate review/calibration is same-agent, informed by external parent review; no independent sign-off on all revised tasks is claimed.

**S008:** existing base/E1/E5, 24 greedy supplied-value answers, four fixed cases per task. Base 22/32, E1 23/32, E5 22/32; each fully solves three of eight tasks. One E5 run-length response uses type placeholders and is unscorable JSON, not four demonstrated arithmetic mistakes. All attempts finished; 179.39 seconds total, 90.48 seconds generation, 654 output tokens. No optimizer updates.

E5 improves the selected row-major outputs specifically, but interval/grid/XOR and literal Unicode errors remain. Unicode code-point versus displayed-grapheme ambiguity needs explicit wording in future probes. S008 changes inputs/format/decoder/budget relative to S006; no single-factor comparison between them.

All jobs exited. Temporary process-scoped keep-awake ended; no persistent power settings changed. Per-process Windows memory sampling produced no usable data; do not infer shared-memory spill.

## Authoritative data and overlay

- Parent snapshot: dataset-v1/candidate-006, unchanged; its old approved exports and adapters remain preserved.
- Repair: dataset-v1/candidate-007. SHA256 of its SHA256.json:
  3fb896ac4454be77d7ea98a777a50678e9ca4824d8dfe5572ad8aae4a6f438f5.
- S007 initially validated hash 479223aaa7abad214421266f23084e3169b996e77857e0354f2431974aaae722. A documented metadata-only finalization corrected inherited counters/status fields. The certificate binds the final hash to unchanged executable sources, cases, prompts, answers and fixtures.
- Executed gold copies have Windows CRLF versus source LF; normalized UTF8 text and AST match. Reference/mutant execution copies match bytes. Do not call this a model-quality change or silently rewrite execution files.
- candidate-007 training packets are model-packets/training-requests.jsonl, containing system/user/assistant chats. Development requests have no assistant answer; gold answers remain in development task TARGET.md files. Only TR records may enter optimizer batches.
- Apply the fit overlay explicitly: studies/S007-measurement-repair/length-preview-002/messages.json replaces the complete TR058 chat. Its file SHA256 is a7c371adde4cb9ece63cb80f07fbcfb5b5ebbb14c8ff6210550df79b45e3a2ca.
- Original TR058 chat 2852 tokens; first preview 2176 did not fit; final preview 1878. All executable AST is preserved except pytest display IDs. Reference plus six mutants produce identical per-case outcome vectors (66 cases each).
- With this overlay and the other 59 chats unchanged, profiled maximum full chat is 2021. This is tokenizer evidence only: no new approved export, exact supervised tokenization or actual backward preflight yet. candidate-007 itself was not overwritten by the overlay.
- CURRENT_CANDIDATE.txt still names the historical corpus. Do not use that pointer to select this study's training data.

## Proposed comparison — freeze before execution

Three inference arms:
1. Pinned base, no adapter.
2. Fresh adapter on calibrated candidate-007 plus the fit overlay.
3. Fresh adapter on the same calibrated examples/fit presentation, with short verified calculation comments beside selected normal-return training rows.

Select comment families and exact expressions from training contracts/oracles before new model outputs. Preserve cases, assertions, expected values and executable AST. Never use failed development outputs as training targets. Comments are visible authored explanations, not fabricated hidden-reasoning traces.

Keep prompts, task IDs/order, splits and development evaluation targets identical across the two trained arms. If comments need additional presentation compaction, apply the same AST-preserving transformation to both arms before freeze. Do not truncate or silently extend 2048.

Use two fresh trajectories from the pinned base; do not resume qwenny-001/002. Match initial adapter/RNG state and shuffle order. Save E1/E3/E5 for provenance; E5 is the predeclared endpoint, not a pool for post-hoc selection.

Starting training settings to retain: seed 42; rank 4 / alpha 8, query/value adapters in eight full-attention blocks (557,056 trainable parameters), dropout 0; AdamW 1e-4, weight_decay 0.01, clip 1, accumulation 4, batch 1, three-update warmup; five passes/300 microbatches/75 updates. See training-v1/PLAN.md and runtime.py for exact prior values. Fixed updates do not mean equal supervised tokens or FLOPs when comments add tokens; record costs.

Primary proposed full-suite outcome is reference-valid first attempts. Report completion/collection, requirement evidence, task-macro mutant results, strict calibrated acceptance and prose separately. No eligible mutant credit for reference-invalid suites. Use the visible eight-task pool provisionally (TR024/TR025/TR038/TR049; DV008/DV004/DV011/DV007), separating familiar from development tasks. Resolve/freeze exact measures and compute ceiling before running.

Proposed matched inference: direct answer, seed 42, temperature 1 / top_k 20 / top_p 0.95, presence 0 / repetition 1, cap 2048 / context 16134, explicit stop IDs. This differs from S008 greedy / cap 512. New matched base attempts are necessary; prior incompatible outputs are not substitutes. No repairs, retries or best-of-N.

## First implementation tasks, in order

1. Verify this handoff's source fingerprints, candidate hash/certificate and overlay. Create a new studies/S009-value-comments work area; preserve all earlier artifacts.
2. Materialize baseline and comment treatment packets with per-record provenance, exact treatment selection and comment verification. Same training IDs/order; development targets never enter optimizer input.
3. Build a strictly hash-bound export/preparation adapter for the new formats. Preserve approval guards and wrong-hash rejection. Accurately record existing authorization/delegation; do not claim that a user reviewed unseen comment text or silently copy an old corpus approval.
4. Validate both target variants against unchanged references and all designated mutants; assess gold against the same explicit rubric as model answers. Record comment expression checks and AST equivalence. Reprofile full chats for both variants.
5. Reuse/extend exact answer-only masking logic, verifying every decoded supervised span equals the visible answer plus im_end. Mask prompts, roles and empty thinking wrapper. No truncation.
6. Implement and validate a model-suite v2 scorer before costly training. S007's meaningful-source predicate is advisory and gold-specific, not a general semantic verifier. Gold witness node IDs cannot be directly matched to arbitrary model-test names: bind relevant failures to actual model test inputs/requirements and inspect/hash-bind generated source before isolated execution.
7. Freeze a complete S009 protocol with variants, hashes, IDs, inference order/settings, metrics, stopping rules, GPU/time ceiling and interpretation branches. Then run actual longest-example forward/backward, masked standard/chunked loss/gradient agreement, intended-adapter-only gradient checks and generation smoke checks.
8. Only after gates pass, train fresh arms, verify fresh imports against saved probes under predeclared tolerances (report actual max difference), run matched first attempts and synthesize results. Do not loosen tolerances or choose checkpoints after seeing failure.

For genuinely missing authorization, finish the concrete reviewable packet first and identify the exact unresolved scope. Do not repeat already-given local training authorization merely because old immutable placeholders say pending; user delegation and prior instructions must be considered accurately.

## Legacy compatibility traps

- dataset-v1/export_reviewed.py expects training-candidates.jsonl and validation.dataset_hash_manifest_sha256. candidate-007 uses training-requests.jsonl; S007 summary stores candidate_manifest_sha256 for the initial snapshot, with final binding in the calibration certificate. A rename or bypass is not a valid export.
- training-v1/prepare_data.py main hardcodes training-approved-001, candidate-006 and output locations. Its encode_answer helper is useful; its main is not ready for the new study.
- train.py defaults to prepared-001 and asserts 60 train / 24 development rows. Pass fresh inputs explicitly, and deliberately retain/document the 12-task A/B loss views or version that interface; do not fabricate duplicates to satisfy an assertion.
- Old generation/scoring scripts have hardcoded adapter paths, prompts and credit rules. Version their S009 bindings. S008's pure JSON scorer measures supplied values, not pytest-suite acceptance.
- On Windows, the first threaded directory-creation validator hit access errors. S007 validate_repair_v2.py uses main-process file setup/logging and bounded parallel pytest subprocesses successfully. Preserve infrastructure failures separately.
- The new wrong-exception policy credits declared related validation-class mismatches at contract-invalid inputs; unrelated crashes on valid-input value tests remain ineligible. S006's old conservative score remains unchanged.
- Comments alone are not established as effective. Do not substitute falling loss for executable results or use a tiny pilot to declare general aptitude.

## Local runtime and boundaries

Model Python: lora-feasibility/.venv/Scripts/python.exe.
Scoring Python: C:/Users/jalar/AppData/Local/Python/pythoncore-3.15-64/python.exe (pytest 9.2).
Pinned Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a.
Torch 2.14.1+cu126, Transformers 5.22.1, PEFT 0.21.2; see lora-feasibility/packages.lock.txt.
NF4/BF16 runtime with frozen CPU input embedding, CUDA transformer/head/adapters, chunk 128 loss. Existing load guard requires at least 8 GiB free on RTX 3080. im_end 248046 / endoftext 248044 both stop generation.

One GPU owner. Local hardware only. No cloud, app closure, persistent power changes, working-model replacement, merge/GGUF export or LM Studio automation. User operates LM Studio. Original GGUF lineage to the pinned training base is unestablished.

Final/regression contents stay reserved. All 12 development targets have teacher-forced loss exposure; six task IDs have full-suite generation exposure and the selected four development tasks also have value-only exposure. DV007 is near the training grid family; do not claim distant transfer. Any eventual final adoption comparison still needs a strong prompted-base arm, frozen task/seed aggregation, uncertainty and regression evaluation.

## Completion and communication contract

At the next study's end, update START_HERE, current state, study register, decisions and backlog. Save all first attempts, partials, raw tokens/settings/prompts, code/source hashes, evaluation logs, cost/memory evidence and review limitations. Write a new observer report explaining what changed, what worked, what remains uncertain and the next decision. No winner may be selected from loss alone.

Start by verifying sources and implementing the missing preparation/scoring gates, not by invoking the old trainer defaults.

