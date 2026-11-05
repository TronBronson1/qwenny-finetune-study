# A repaired measuring system, then a smaller model test

Report 005 • November 4, 2026

I carried the program through two steps: repairing the measurement/data design, then testing the existing models on supplied inputs. **The measuring system is stronger, but we have not yet established a reliable Qwenny upgrade.**

## What we repaired

A new, separate candidate contains the 60 training and 12 development tasks. The original dataset and S006 results remain intact.

The repair fixes the demonstrated ASCII-digit, case-sensitivity and subclass gaps, and the generator's omission of ordinary wrong-type elements. It also clarifies return types, removes irrelevant instructions from scalar tasks, and gives the gold answers task-specific coverage mappings. Additional cases cover issues such as preserving input order and merging several intervals.

Every revised gold suite passed its correct function: 1,475 test cases. All 407 designated defective versions were rejected through concrete checks. Five negative controls also behaved as intended: empty tests, pass-only tests, skipped tests, vacuous assertions and unrelated crashes did not earn success.

Those numbers show calibration within a finite benchmark. They do not prove that every possible defect is covered, or that 407 fixtures represent independent kinds of intelligence. Review remains same-agent, informed by the independent review; the revised corpus has not received a new independent sign-off.

## Keeping ordinary hardware in view

One expanded training example reached 2,852 tokens, above our previous 2,048-token capacity. I did not cut its tests or enlarge the budget.

A separate presentation preview retained every executable case and assertion while reducing it to 1,878 tokens. It produced identical individual test outcomes against the reference and all six defective versions. With that explicitly documented overlay, the largest profiled training chat is 2,021 tokens.

This is a viable length plan, not a new training run. Export checks, answer masking and an actual longest-example backward check are still required before training.

## What the smaller model test asked

Instead of asking Qwenny to invent tests, I supplied four concrete input cases for each of eight already-visible tasks and asked only for the return values.

We tested the original base, E1 and E5 using one greedy first attempt each. No answer was repaired or retried. No new weights were trained.

| Existing model | Correct supplied values | Tasks with all four values correct |
|---|---:|---:|
| Base | 22/32 | 3/8 |
| E1 | 23/32 | 3/8 |
| E5 | 22/32 | 3/8 |

A format failure counts as zero in that first column and is identified separately. E5 gave type placeholders rather than concrete JSON for one run-length task; those four values were unscorable, not four proven calculation mistakes.

The small differences do not identify a winner.

## What we learned

The models can answer some supplied-value questions well. All three got the selected uppercase and hexadecimal cases right. E5 got all four grid-offset cases right, where base got one and E1 got two.

But errors remain without pytest-writing work. All three mishandled one XOR cancellation case. Interval merging and grid neighbors were unreliable. All three treated two visually similar Unicode representations as identical, despite the literal code-point comparison expected by the reference.

That last example also teaches us to write more precise prompts: a displayed accented character and a letter plus combining accent can look the same. Future tests should distinguish representation ambiguity from other kinds of error. This run stays unchanged.

The model run took about three minutes, including verification/loading; generation itself took about 90 seconds. All 24 responses completed. The repaired gold validation took about 3.4 minutes, plus preparation, profiling and documentation time.

## What comes next

A useful next training experiment should focus on constructing correct return values, using reviewed examples and perhaps short verifiable calculation comments. It should be a controlled comparison against the calibrated baseline, not another unstructured increase in epochs.

Before training, we must explicitly package the fit overlay, check the supervised answer tokens and run the actual longest-example preflight. The current adapters were trained on the old corpus; none of this repair has silently changed their weights.

Final and regression tasks remain reserved. S006's historical scores are unchanged, and no retrospective first success has been awarded.

## New terms

- **Calibration:** checking that our examples and scoring behave correctly on known good and deliberately bad cases.
- **Negative control:** an input or test that must not earn success, used to catch a flawed measuring system.
- **Greedy decoding:** choosing the highest-scoring next token at each step.
- **Component diagnostic:** testing one part of a larger skill—in this case, supplied return values instead of complete test design.
- **Code point versus grapheme:** a character encoding unit versus a displayed character; one visible character can contain multiple code points.
- **Training overlay:** an explicit, versioned replacement for part of a dataset, with its own provenance.

[Measurement repair results](../studies/S007-measurement-repair/RESULTS.md) · [Fixed-input results](../studies/S008-fixed-input-values/RESULTS.md) · [Current program state](../program/CURRENT_STATE.md)

