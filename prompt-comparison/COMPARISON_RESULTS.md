# Development comparison results

User operates Qwen; Codex preserves responses and executes evaluation. Current prompt/settings and seed 42 requested throughout; effective settings and exact submitted inputs are not independently verified. Timing/tokens/stop reasons not supplied. This is a small development check, not final held-out evaluation.

| Task | Arm | First attempt | After at most one repair | Repair reference result |
| --- | --- | --- | --- | --- |
| T01 rotation | A: instructions | Fail: syntax/collection | Fail | 32 passed, 3 failed |
| T01 rotation | B: two demonstrations | Fail: syntax/collection | Fail: syntax/collection | No test bodies executed |
| T02 clock parsing | B: two demonstrations | Fail: missing exact-int assertion; 16 reference tests pass, 5/5 mutants detected | Fail: isinstance accepts int subclasses | 16 passed, 5/5 mutants detected |
| T02 clock parsing | A: instructions | Fail: missing exact-int assertion; 15 reference tests pass, 5/5 mutants detected | Pass | 15 passed, 5/5 mutants detected; exact-int asserted |

T01 suites are reference-invalid; their mutant detection scores are ineligible. Both T02 first attempts are reference-valid and detect all five fixed mutants, but lack the original contract's exact-int result assertion and therefore miss strict task acceptance. B's repair also misses exact type; A's repair supplies it and passes. Do not compare raw test counts as accuracy.

| Acceptance measure | A: instructions | B: two demonstrations | B minus A |
| --- | --- | --- | --- |
| First attempt | 0/2 (0%) | 0/2 (0%) | 0 percentage points |
| After at most one repair | 1/2 (50%) | 0/2 (0%) | -50 percentage points |

Paired first attempts: two ties, no wins/losses. Paired one-repair outcomes: one A win and one tie, no B wins. Reference-valid suites detecting all fixed mutants: 1/2 tasks per arm at both stages. Both arms used one repair per task (two repairs per arm). Generation time/tokens and manual handling time were not measured; no cost/speed comparison is available.

No accuracy benefit from these two demonstrations was observed in this development check. A's one-repair strict acceptance was higher, but two task families at one intended seed are insufficient to infer that demonstrations generally harm accuracy. Responses and feedback are visible development material; do not reuse these families as unseen final tests. Sampling/loading identity and exact inputs were user-operated rather than independently captured. Frozen references/mutants were authored and agent-checked; second-person review remains pending. Identical repair policy was used, with task/answer-specific category feedback, so feedback content differs between arms. No trained adapter or weight change was evaluated.

Prose review: no affirmative execution claims, but both arms overstated coverage. B's repaired answer claimed object-reference comparisons absent from its assertions. Individual reports and complete execution logs are in `../runs/comparison-T01-A/` and `../runs/comparison-T01-B/`.

Status: comparison complete. Preserve all examples, inputs and results. LoRA remains the first planned weight alteration. Next milestone is the training feasibility check in `../02_MACHINE_AND_TRAINING.md`: establish compatible model identity/runtime, then a measured adapter forward/backward/save/reload trial before a full training run. When evaluating an adapter in another runtime, repeat matched A/B controls there; this LM Studio pilot alone cannot isolate a cross-runtime weight effect. The two demonstrations remain checked training candidates, awaiting independent human review; they are not a sufficient training dataset.
