# The missing tests are now demonstrated

Report 004 • November 4, 2026

The follow-up review supplied stronger evidence than keyword warnings. It created deliberately broken versions of functions and showed that our gold tests still passed them.

I replayed all eight saved experiments on the CPU and confirmed a concrete wrong behavior in each broken version. The results matched the reviewer’s.

## What this establishes

Five gold suites missed violations of ASCII-only digit rules. One missed case sensitivity, one missed integer-subclass endpoints, and an additional example missed an ordinary wrong-type element. For that last example, the broken function accepted a one-item list containing a string and returned an empty list instead of raising the required error.

These are demonstrated blind spots. An automatic flag alone would not have established them; the checker also produced false positives.

Four of the seven main gaps are in training targets, and three are in development targets. Development answers were not used to update the adapter. The additional ordinary-element example is a training task.

The saved evidence demonstrates eight specific cases. The broader claim about 16 ordinary-element gaps still needs the remaining task-level confirmations. Most tasks still need a person to review their particular meaning.

## What this means for the apparent near-success

E5’s edit-distance answer passed the correct implementation and all three original defective versions. Its recorded coverage rejection concerned case sensitivity—a check the gold example also lacked.

That is a consequential grading problem. We will not quietly change its old result to a pass. We also should not delete an explicit case-sensitivity requirement merely to obtain a success.

The better repair is to improve the example, add a meaningful case-sensitivity defect, and make the scoring policy clear in a new version. If we later compare old answers under revised rules, that will be labeled a post-hoc sensitivity analysis, not a fresh success.

## Next steps

Prepare a separately versioned repair to the examples and evaluator. Require every gold answer to satisfy the same applicable instructions and rubric as the model, pass the correct function, and detect all designated defective versions through meaningful checks.

The new defective copies need validity review before becoming official benchmark items. More mutants help make requirements executable, but a finite collection still cannot prove complete coverage.

No GPU work, model training or model-answer rescoring occurred. The original dataset and S006 evidence remain unchanged. The useful scratchpad evidence has been preserved in the program folder.

## Two useful terms

- **Behavioral witness:** a concrete input that shows the broken version behaves differently from the correct one.
- **Surviving mutant:** a deliberately defective version that a test suite fails to reject. It exposes a blind spot in those tests, provided the defect itself is valid.

[Detailed evidence and next gate](../program/reviews/review-002/README.md) · [Previous correction](REPORT_003.md)

