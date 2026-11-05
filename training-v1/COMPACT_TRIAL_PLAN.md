# Compact-target ablation 001 — declared before training/generation

Motivation: supplied-answer likelihood improved without free-running correctness.
Test whether reducing target presentation overhead helps completion/correctness.
This bundles case-ID removal, whitespace and prose shortening; it cannot isolate
which component matters. Executable AST remains identical except pytest display
IDs. Every training input, expected value, assertion, exception check and helper
is preserved. Development targets are byte-identical to prepared-001.

Data: prepared-compact-001, same 60 reviewed training tasks/prompts/order/splits.
Total supervised tokens 30,660 versus 39,730 (22.83% reduction); maximum complete
training input 1,578 versus 1,954 tokens. Original corpus and exports preserved.
Validate original/compact runtime outcomes on every training reference and
designated mutant before proceeding. Final tasks/regressions are not accessed.

Training: fresh same pinned base (not continued from E5), same seed42, LoRA
rank4/alpha8 q/v full-attention scope, CPU frozen embedding, NF4/BF16 runtime,
batch1/accumulate4, LR1e-4, first3-update warmup, AdamW/weight decay/clip and
shuffle schedule unchanged. Five epochs, 300 examples/75 optimizer updates;
save checkpoints1/3/5. Equal examples/updates, not equal token exposure or compute.
Use unchanged train.py with --prepared prepared-compact-001 --run runs/qwenny-002-compact.
Existing corpus-level local-training authorization plus user's carry-on applies
to this presentation-only derivative; no fabricated new per-record review.

Primary pilot: final E5 checkpoint only, same already-visible DV001/DV002 messages
as gap-001. Direct-answer, sampling seed42/temp1/topk20/topp.95, presence0,
repetition1, cap2048, context16134, explicit im_end/endoftext stops. One first
attempt per task, no repair/retries. Compare existing base and original-E5
sample0 results, both 0/2 accepted. Fresh-import verify all three saved checkpoints.
Do not choose a different epoch based on these two outputs or present a winner.

Outcomes: format/completion/length, syntax, reference validity, frozen3-mutant
detections conditional on valid reference, and separate requirement/prose review.
No raw loss comparison between different training target formats. Original-format
development teacher-forced loss is still a secondary common-target diagnostic.
Any gain on two visible families is exploratory, not general aptitude evidence.
Broader development, thinking-enabled and deployment controls remain outstanding.
