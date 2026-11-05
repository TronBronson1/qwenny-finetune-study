# Latest status — 2026-11-03

User selected the LOCAL RTX 3080. Do not switch to cloud or incur rental costs.

Latest, 2026-11-04: ../training-v1/COMPACT_TRIAL_RESULTS.md and
../HANDOFF_COMPACT_TRIAL.md. Compact-target derivative preserves all substantive
checks, uses22.83% fewer target tokens, and passed 480 paired pytest executions.
Fresh local training qwenny-002-compact completed; three adapters saved/import-
verified with exact probe logits. E5 pilot0/2: both complete but syntax-invalid.
All jobs finished. Next thinking-enabled matched controls remain unperformed.

Latest investigation: ../training-v1/investigations/gap-001/README.md and
../HANDOFF_GAP_INVESTIGATION.md. Eight new matched direct-answer outputs completed
and were reviewed/scored: zero reference-valid/strictly accepted, three truncated.
Four original presence-1.5 outputs were reused. Removing the penalty did not close
the likelihood/correctness gap. No new training, final-test access or model changes.
GPU work is finished; remaining training/deployment controls are not yet done.

Latest: the first real training run is complete. See ../training-v1/README.md and
../HANDOFF_TRAINED_QWENNYS.md. E1/E3/E5 adapters trained, saved and freshly imported
with exact checked logits. Training/checkpoint development evaluation took about
11.6 minutes. A bounded two-family direct-answer pilot showed no strict acceptance
gain despite lower development loss. No candidate adopted or LM Studio GGUF replaced.
All GPU jobs have exited. Earlier fit/assembly status below is historical.

Latest update: the 2048-token fit check passed with explicit frozen input-embedding
placement in CPU RAM. See FIT_2048_RESULTS.md and fit-2048-summary.json. Three
updates took 4.312/4.328/4.500 seconds, training-stage CUDA free memory stayed
above about 799 MiB, and sampled process shared usage peaked at 82 MiB. Adapter
save/fresh reload matched checked logits exactly. The all-CUDA 2048-token baseline
was interrupted during backward after sustained paging; it did not establish fit.
User corpus-level review sign-off is recorded in ../dataset-v1/USER_REVIEW_2026-11-03.json.
No apps were closed and no full task-training run has started.

Earlier 768-token measurements and assembly-stage status follow; use the latest
2048-token report for the current memory layout and timing.

The compatibility, realistic-length capacity and short repeated-update benchmark
are complete. Meaningful task training has NOT started: no reviewed corpus is frozen.

- Earlier 64/128-token synthetic trials passed and remain preserved.
- Current candidates measure 752/767 full-chat tokens; neither was used as training data.
- Standard 768-token trial passed but exhausted device headroom; user observed about
  1 GB shared-memory overage. Its 40.547-second step was paging-affected.
- Checkpointed chunked loss preserved all tokens and passed bounded loss/gradient checks.
- The chunked 768-token ten-update benchmark passed all updates and save/reload.
- Mean update 2.033 seconds; median excluding first two 1.945 seconds.
- Windows process GPU counters showed 82 MiB peak shared usage during 13 valid
  training-phase samples. No 1 GB spillover was observed in that interval.
- CUDA stage free memory still fell to 173 MiB; nvidia-smi sampled free reached
  545 MiB. Treat headroom as limited, with no larger-context/long-run guarantee.
- All trial and monitoring processes exited. Existing models/results are preserved.
- All adapters so far are disposable synthetic artifacts, not Qwenny quality candidates.

See REAL_LENGTH_RESULTS.md and timing-summary.json for evidence and limitations.
For a hypothetical 60-example, three-pass pilot at this length and adapter scope,
compute arithmetic is about six minutes; provisionally allow 15–30 minutes for
training/loading/checkpoint checks. Dataset authorship/review and evaluation are extra.

Dataset assembly is now complete: see ../dataset-v1/README.md and
../HANDOFF_DATASET_ASSEMBLED.md. Current review candidate is candidate-006:
60 training / 12 development / 24 final / 12 regression tasks. All independent
review is pending. Full training chats reach 1954 tokens, beyond the 768-token benchmark.

Next: independently review the assembled family-split corpus, freeze source hashes
and the reasoning policy, validate assistant-only masking and complete targets, and repeat matched
base A/B controls in the chosen runtime before attributing changes to LoRA.
Initial planning targets: 60 training / 12 development / 24 final / 12 regression tasks.
D01/D02 independent review remains pending. Keep visible development families out
of final evaluation and exclude failed Qwen answers from training targets.

No cloud rental/upload/account was started. LM Studio chats remain user-operated.
Merge/export/GGUF compatibility remains a separate, untested step.
