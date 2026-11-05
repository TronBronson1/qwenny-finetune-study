# Latest Qwenny handoff — compact-target trial complete

2026-11-04 America/New_York. User said to carry on. Prior exact-base/environment/
authorization details remain in HANDOFF_TRAINED_QWENNYS.md; likelihood-gap study in
HANDOFF_GAP_INVESTIGATION.md. Read training-v1/COMPACT_TRIAL_RESULTS.md next.

Prepared a presentation-only derivative of the same 60 approved training tasks.
All executable AST preserved except pytest case display IDs; whitespace/prose
shortened. 22.83% fewer supervised tokens. Development tokenized targets unchanged.
Original corpus/exports/models/results preserved. Paired original/compact pytest
outcomes identical on all 60 correct and 180 mutant implementations (480 runs).
All 1,035 reference tests pass. No final/regression targets used.

Trained fresh qwenny-002-compact with unchanged seed42/base/LoRA/optimizer/
examples/update schedule: 5 epochs,300 examples,75updates,608.281s training+dev eval.
E1/E3/E5 saved; fresh imports all exact probe logits (max abs0). Separate packages
under training-v1/candidates/qwenny-002-compact, never overwriting qwenny-001.
Peak allocated6.78GiB/reserved7.54GiB, sampled min free764MiB, shared process82MiB.

Predeclared E5-only sample0 direct-answer pilot on same DV001/DV002, seed42,
temp1/topk20/topp.95/presence0/repetition1/cap2048/context16134. Both outputs
complete (530/537 tokens), both syntax-invalid,0/2 reference-valid/strict accepted.
Further contract errors visible without repair. Source inspected/hash-bound
before isolated unchanged reference/mutant evaluator. No retries/best-of-N.
Original E5 sample0 was also0/2 (520/931tokens). Cannot rank general aptitude.

Compact E5 common original-format dev loss A/B .54489/.49732 versus original E5
.13293/.22185. This format-sensitive diagnostic is not execution correctness;
compact-format training losses are not directly comparable with original ones.

All jobs exited. No cloud, app closures, LM Studio changes, merge or GGUF export.
Original GGUF lineage issue remains; adapters not deployment-tested GGUFs.

Next: matched thinking-enabled base/adapted control on development data before
additional training. Not yet performed. Keep first attempts and config distinctions,
final families untouched, and no failed development outputs as training targets.
Do not silently increase generation cap or repair failures in scored results.
