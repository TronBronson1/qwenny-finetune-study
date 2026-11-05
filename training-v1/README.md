# Qwenny training v1 — trained and import-verified; quality gain not demonstrated

> **Latest — November 4, 2026:** [S007](../studies/S007-measurement-repair/RESULTS.md) repaired/calibrated data without training. [S008](../studies/S008-fixed-input-values/RESULTS.md) tested existing base/E1/E5 on 32 supplied values each: 22/32, 23/32, 22/32, including one E5 format failure. No model adopted and no new optimizer updates. [Observer Report 005](../observer/REPORT_005.md). Earlier “latest” entries below are chronological history, qualified by the adversarial review.

> **Latest completed study — November 4, 2026:** [S006 results](../studies/S006-learning-and-transfer/RESULTS.md) cover four familiar training and four development tasks, base/E1/E5. All 24 answers finished; none strict accepted, 8 reference-valid, 5 met the conservative all-three-mutant rule. No additional training. [Observer report](../observer/REPORT_002.md). The older next-step statements below are historical; consult [current state](../program/CURRENT_STATE.md).

> **Previous milestone — November 4, 2026:** The [matched thinking-enabled control](THINKING_CONTROL_RESULTS.md) completed with base, original E5 and compact E5 each 0/2 strict accepted; five of six outputs hit the 8192-token cap. It led to S006, now complete above. References below to thinking control as future work are historical.

Latest, 2026-11-04: [compact-target training trial](COMPACT_TRIAL_RESULTS.md)
is complete. Same 60 tasks/checks with 22.83% fewer supervised tokens; all paired
reference/mutant outcomes preserved. Three additional adapters trained and fresh-
import verified. Predeclared E5 pilot: both answers complete, both syntax-invalid,
0/2 accepted. No candidate adopted. All jobs finished; final tasks remain untouched.

Latest: [the likelihood/generation gap investigation](investigations/gap-001/README.md)
is complete. Eight new matched direct-answer outputs plus four original outputs
showed no accepted answer on the same two development tasks. Removing the presence
penalty did not close the gap; greedy decoding produced three truncated answers.
No further training was performed, and final-test tasks remain untouched.

Three experimental adapters are saved: **Qwenny E1, E3 and E5**, after 1, 3 and 5
passes through the same 60-task corpus. They are checkpoints on one trajectory,
not independently trained models or verified tiers of aptitude. All three loaded
into a fresh base and reproduced stored probe logits exactly.

## Artifacts

- [Qwenny E1](candidates/qwenny-001/Qwenny-E1/README.md)
- [Qwenny E3](candidates/qwenny-001/Qwenny-E3/README.md)
- [Qwenny E5](candidates/qwenny-001/Qwenny-E5/README.md)
- [Training settings and scope](PLAN.md)
- [Training report](runs/qwenny-001/report.json)
- [Complete first-attempt generation records](probes/qwenny-001-direct-001/report.json)
- [Execution score](scoring/qwenny-001-direct-001/summary.json)
- [Agent acceptance review](scoring/qwenny-001-direct-001/agent-acceptance-review.json)
- [Exact-output-type diagnostic](diagnostics/qwenny-001-exact-int-gap/report.json)
- [Cached/full-forward diagnostic](diagnostics/qwenny-001-cache-001/report.json)

Each candidate has the exact adapter_config.json and adapter_model.safetensors
copies, SHA256 fingerprints and provenance. The adapter weight file is 2232928
bytes. Base weights remain separate and unchanged on disk. The pinned base is
Qwen/Qwen3.5-9B at c202236235762e1c871ad0ccb60c8ee5ba337b9a.

## Training and loss

The local run completed 300 training microbatches / 75 optimizer updates, with
every training task used exactly five times. It took about 11.6 minutes from the
start of optimizer training through checkpoint development-loss checks; loading,
preflight, base controls and generation scoring are extra. Median training
microbatch time was 2.0 seconds. No base parameters received gradients, intended
adapter gradients were finite/nonzero, and every optimizer update changed them.

Assistant-only tokenization was checked on every example. Full answers and im_end
were supervised; prompts/roles/empty thinking wrapper were ignored. Nothing was
truncated. The actual longest example completed backward before optimizer training,
and cached generation terminated correctly in the smoke check.

| Weights | Instruction-only prompt loss | With fixed demonstrations loss |
|---|---:|---:|
| Base (A/B) | 0.8934 | 0.7899 |
| E1 (C/optional D) | 0.7698 | 0.7082 |
| E3 (C/optional D) | 0.3816 | 0.4306 |
| E5 (C/optional D) | 0.1329 | 0.2218 |

These are mean per-example teacher-forced assistant-token losses on the 12
development targets. The labels/answers were never optimizer training data.
Likelihood improved, but the free-running results below show why it is not a
substitute for executable acceptance or reasoning/regression evaluation.

Training-stage allocator peaks were about 7.07 GiB allocated / 7.57 GiB reserved.
CUDA-reported free memory reached about 414 MiB at a recorded microbatch stage;
Windows process shared usage peaked at 82 MiB over the training interval. All
300 microbatches completed without reported OOM/nonfinite-gradient failure, but
headroom is still limited and desktop occupancy can vary.

## First-attempt generation pilot

This is a **separate bounded direct-answer pilot**, not the historical thinking-on
LM Studio comparison: thinking disabled, seed 42, temperature 1, top_k 20,
top_p .95, output-only presence penalty 1.5, maximum 2048 new tokens. The penalty
implementation is recorded and is not claimed identical to LM Studio's. Exactly
one answer per task/variant was saved; no repairs, retries or best-of-N selection.
The tasks were the already-visible development rotation and clock families.

| Variant | Reference-valid suites | Reference + 3 mutants + complete format | Agent strict acceptance |
|---|---:|---:|---:|
| base-A | 0/2 | 0/2 | 0/2 |
| base-B | 0/2 | 0/2 | 0/2 |
| epoch-1-C | 1/2 | 1/2 | 0/2 |
| epoch-3-C | 0/2 | 0/2 | 0/2 |
| epoch-5-C | 0/2 | 0/2 | 0/2 |

The only provisional executable success was E1 on clock parsing. It still used
isinstance(result,int), allowing non-bool int subclasses. A separate post-hoc
diagnostic implementation returns such a subclass: all 24 generated tests pass,
while the gold suite detects it. This diagnostic validates a pre-existing explicit
requirement; it is not added to the frozen three-mutant denominator.

Other answers had collection errors, incorrect expected values/exceptions, wrong
arity or syntax errors. E3's rotation answer hit the cap without closing its code
block. Cutoff responses and reference-invalid suites were not credited with mutant
scores. All complete code blocks were read and hash-bound source inspection was
recorded before isolated execution. Original answers were never repaired or altered.

Two task families and one seed are insufficient to rank general aptitude. The
zero strict passes show no acceptance gain in this pilot; they do not prove
training is universally harmful, establish that quantization caused the errors,
or measure behavior under thinking-enabled inference. The 24 final tasks and
broader regression set have not been evaluated by these models.

## Cache and deployment compatibility

Fresh adapter import is verified. A read-only cache diagnostic compared raw cached
decoding logits with full-context forwards on five positions from each of base
and E5. Top-token choices matched 5/5 for both; maximum KL was about 0.00190 and
0.00123 respectively. Raw logits were not bit-identical (largest absolute
differences 0.5625/0.75). This bounded result showed no gross mismatch at those
positions; it does not rule out all long-sequence/cache/numerical issues.

These are PEFT adapters, **not standalone LM Studio GGUF models**. The documented
LM Studio import route takes model files such as GGUF. Merge/conversion and matched
requantized base/adapted validation remain a separate stage. No working LM Studio
model/settings were replaced and no cloud rental or upload was started.

## Decision

Retain both sets of three experimental candidates and the working base. Do not
adopt a checkpoint on the loss table alone. The decoding/loss-decomposition and
compact-target training investigations are complete (linked above). Next test
matched thinking-enabled inference before more training or claims about the
original LM Studio workflow.
Keep final-test families untouched until a candidate/protocol is frozen. No
general coding or reasoning improvement is claimed.
