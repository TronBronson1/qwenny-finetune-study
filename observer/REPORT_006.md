# The training comparison stopped before it could answer the question

Report 006 • November 4, 2026

**We prepared and tested the controlled experiment, but did not finish the model comparison.** The first training run slowed sharply and reached its declared 20-minute limit. I stopped there, preserved the evidence and did not start the second run or score replacement checkpoints.

## What we were trying to learn

The question was whether short calculation notes help Qwenny write correct tests. We prepared two versions of the same 60 training examples. One has the calibrated answers; the other adds 23 short, checked calculations for digit sums, bit counts, hexadecimal values and grid offsets.

For example, a grid-offset note can show `1*3+2 = 5`. The examples keep the same cases and assertions. We planned to train both versions from the same starting model and then compare their final checkpoints with the unchanged base model.

## What worked

The data preparation and measuring system passed their checks. Both training packets passed against their correct functions and detected all their designated defective versions. The new scorer also handled known good answers with renamed tests and rejected six deliberately inadequate controls.

Every training answer fits the existing length limit. The larger packet reaches 1,920 tokens, below 2,048. We verified exactly which answer tokens contribute to training and kept development answers outside the optimizer.

Both versions also passed real hardware preflights: the longest example could run forward and backward, the two loss calculations agreed within the fixed rules, and a small generation check finished correctly. The two fresh initial adapters were identical.

One useful preparation discovery involved Unicode. The tokenizer can normalize a combining accent and silently change a literal-character test. Writing that character with an explicit Python escape preserved the test's meaning. The original dataset was left intact.

## Where execution stopped

The baseline run completed 213 logged examples and 53 updates, against the planned 300 examples and 75 updates. It saved its first- and third-pass checkpoints, but never reached the required fifth-pass checkpoint.

Completed batches had typically taken about 2.7 seconds. Near the slowdown, reported free CUDA memory reached zero and the few subsequently completed batches had a median time of about 34 seconds. The next batch did not finish before the deadline.

That timing pattern is evidence to investigate. It does not prove why the slowdown happened. The separate Windows process-memory sampler again supplied no usable measurements, so I cannot identify another application or claim that memory spilled into system RAM.

The controller stopped the run at the original limit. The second training arm and all 24 planned scored answers were left unattempted. The GPU execution sequence, including both preflights, took about 27 minutes.

## What this means for Qwenny

We cannot say whether calculation comments help or hurt. We also cannot treat the unattempted answers as demonstrated model mistakes. Training loss and partial checkpoints do not answer the comparison question.

No upgrade was selected or deployed. Existing models, earlier studies, final/regression questions and LM Studio were preserved. No apps were closed and no persistent power settings changed.

The next decision is to establish a stable, realistically bounded local runtime before scheduling a new paired training attempt. The prepared examples and scoring checks remain useful; the interrupted run stays in the record.

## New terms

- **Input-bound scoring:** linking a detected mistake to the actual inputs used by the generated test.
- **Answer mask:** the record of which answer tokens teach the model and which prompt tokens are ignored.
- **Preflight:** an actual execution check before committing to training updates.
- **Budget stop:** ending at a previously declared time or resource limit, even when the intended comparison is unfinished.

[Full study results](../studies/S009-value-comments/RESULTS.md) · [Updated glossary](GLOSSARY.md) · [Current state](../program/CURRENT_STATE.md)
