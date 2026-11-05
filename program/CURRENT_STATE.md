# Current state

As of November 4, 2026 (America/New_York). Maintainer: orchestrator.

## Purpose and success

Program goal: improve Qwenny on ordinary hardware through a reproducible, worthwhile study that others can understand.
Current task: specification-to-pytest generation. This is not yet a claim about general coding ability.
Primary quality measure: first-attempt strict task acceptance, with completion, reference validity, mutant detection, contract coverage, and unsupported execution claims reported separately.

The original provisional final adoption rule is in ../01_EXPERIMENT_PLAN.md: at least a 10-percentage-point improvement over the prompted base, no more than one additional regression failure, and no increase in fabricated execution claims. Revisit and freeze the exact aggregation and uncertainty reporting before final evaluation; do not silently revise it after seeing final results.

## Established
**Review correction:** User-supplied independent review identified three gold targets that fail the frozen coverage rubric; direct inspection confirmed them. S006 strict acceptance is a historical rubric outcome, not a calibrated standalone model-capability measure. See [review disposition](reviews/REVIEW_001_RESPONSE.md) and [observer correction](../observer/REPORT_003.md). Execution facts are retained; model-selection conclusions are deferred pending measurement repair.


- Dataset candidate-006: 60 training / 12 development / 24 final / 12 regression tasks.
- User corpus authorization exists; historical pending placeholders do not revoke it.
- Local RTX 3080 training works. Pinned base: Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a.
- Original and compact training trajectories each have E1/E3/E5 checkpoints with exact saved-probe fresh-import checks.
- Lower teacher-forced loss did not establish better freely generated answers.
- Original direct-answer pilot: no strict accepted answers; original E1 clock was executable but missed an explicit exact-type requirement.
- Matched decoding investigation, compact training, and thinking-enabled control are complete.
- Thinking control: base/original E5/compact E5 each 0/2 strict accepted; five of six responses hit the 8192-token cap.
- S006 learning/transfer diagnostic complete: all 24 answers finished; 8 suites reference-valid, 5 met the conservative all-three-mutant rule, none strict accepted. Each model scored 0/4 strict in training and 0/4 in development. See [results](../studies/S006-learning-and-transfer/RESULTS.md) and [observer report](../observer/REPORT_002.md).
- No candidate selected. All reported jobs exited.

## Limits

Earlier repeated generation studies used DV001/DV002. S006 added generation exposure to DV004/DV007/DV008/DV011, still one seed. All 12 development targets have already been used for teacher-forced loss; remaining development tasks are not wholly unseen evaluation.
Historical LM Studio GGUF behavior and Python NF4 behavior are not interchangeable. Quantization has not been isolated as a cause.
Same-agent dataset validation is substantial but does not establish independent semantic review.
Final and regression models' task performance remains unmeasured; keep these splits reserved.

## Current decision

S009 ended at the frozen first-arm wall-time limit. **No paired model-quality comparison was obtained. No job is running, and no candidate was selected or deployed.** Read [Report 006](../observer/REPORT_006.md), [results](../studies/S009-value-comments/RESULTS.md), [terminal evidence](../studies/S009-value-comments/stopped-evidence-001.json), and [next handoff](../studies/S009-value-comments/HANDOFF.md).

Preparation succeeded: 23 oracle/reference-verified comments on TR007/TR010/TR038/TR049; exact provenance/current authorization and wrong-hash guards; same training IDs/order, AST/cases and prompts; masked/decoded assistant-only spans; shared TR049 whitespace compaction. Baseline/comment maxima: 1880/1920 tokens. Both 60-target variants passed 120 reference suites and 664 mutant executions. The input-tracing scorer passed eight renamed gold suites/all 52 selected fixtures and six negative controls. Actual model source/coverage review remains unexercised because no scored answers were generated.

The 12 development targets retain their historical 24 A/B no-gradient loss views. DV008's combining accent is represented by a literal escape with exact AST equality so tokenizer normalization cannot change that target's meaning. No development answer entered optimizer input. The original candidate-007 and old corpus approvals were preserved.

Both real longest-example backward/gradient/generation preflights passed, and their initial adapter hashes matched. The fresh calibrated baseline then logged 213 completed microbatches and 53 updates before its 1200-second arm ceiling. E1/E3 and optimizer/RNG/probes are retained but not fresh-import-verified; no E5. The comment trajectory and all 24 planned first attempts remain unattempted. The controller's terminal record supersedes the forcibly terminated child's last status of training.

Completed batch times slowed as reported CUDA-free memory reached zero; median timings were 2.672 seconds for positive-free samples and 34.352 seconds for four zero-free samples, followed by an unfinished batch. This is an observed association, not an established cause or shared-memory-spill finding. Windows process memory produced no usable rows. Total GPU orchestration, including verification/loading and two preflights, was 27.07 minutes. No timeout extension, retry or partial-endpoint substitution was made.

S007/S008 remain complete and unchanged. S006's historical strict zero is not a calibrated standalone capability measure. All development exposure qualifications and final/regression reservations remain in force. The original handoff and NEXT_TRAINING_STUDY are historical, preserved artifacts.

Next proposed work is a separately frozen local runtime/resource diagnostic with representative sustained work and a justified ceiling before another paired attempt. Do not rerun the stopped S009 controller, resume its partial baseline as a matched fresh trajectory, or inspect reserved tasks to choose a repair. No new GPU work has been launched after the stop. Existing routine design/testing delegation persists; no cloud/app closure/deployment authority is added.

## Operating boundaries

Preserve original data, models, outputs, hashes, and failed attempts. Local hardware only; no cloud, app closure, LM Studio automation, conversion, or deployment under this organizational work.
Never train on failed development answers. Never repair an answer inside its first-attempt score.
Any future final evaluation requires frozen candidate selection, protocol, scoring rubric, and treatment of seed aggregation.

