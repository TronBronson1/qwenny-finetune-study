# Qwenny handoff — matched thinking control complete

2026-11-04 America/New_York. Read training-v1/THINKING_CONTROL_RESULTS.md next.
Prior base/environment/training authorization and compact trial details remain
in HANDOFF_TRAINED_QWENNYS.md and HANDOFF_COMPACT_TRIAL.md.

Matched pinned NF4 base / original E5 / compact E5 on already-visible development
DV001/DV002, instruction-only. Thinking enabled, seed42, temp1/topk20/topp.95,
presence0/repetition1, cap8192 shared reasoning+answer, context16134, explicit stops.
Both E5 import probes exact (max abs0); prompt matching/input hashes verified.

All three models 0/2 strict accepted. Five of six hit cap. Compact both tasks and
original E5 clock never closed thinking/no final answer. Base rotation produced
a complete fence but wrong list inputs (24 reference failures), mapping truncated.
Original E5 rotation terminated at6904 tokens, but undefined nested causes
collection failure. Base clock closed thinking then truncated inside code/no fence.
No repairs, retries, cap increase, best-of-N, or failed-output training targets.

Full first attempts: training-v1/probes/thinking-001. Definitive unchanged execution:
training-v1/scoring/thinking-001-pytest. Initial scoring/thinking-001 used training
Python without pytest; preserved as infrastructure failure, excluded from quality
claims. Same outputs then executed with established Python3.15/pytest9.2.
thinking-control-results.json links final machine results; hashes preserved.

This is bounded Python thinking-on presence0, NOT historical unrestricted GGUF
LM Studio presence1.5. Old direct-answer2048 comparisons confound mode/budget.
Two visible families/one seed cannot rank aptitude or justify quantization blame.
No winner selected and no additional training performed. Keep final/regression
tasks untouched until candidate and final protocol are frozen. Any next development
configuration must be separately predeclared, never a rescue of these attempts.

Generation and scoring jobs exited. Temporary process keep-awake ended. Existing
models/results preserved; no cloud, app closure, LM Studio changes, merge or export.
GPU-wide logs available; Windows per-process shared-memory samples unavailable.
