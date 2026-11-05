# An important correction after independent review

Report 003 • November 4, 2026

**The review found a real weakness in our measuring system: some of our gold examples did not meet the same coverage rules we used to judge Qwenny.**

I checked the three cited examples and confirmed them. Our hex-byte gold answer did not test non-ASCII digits; our edit-distance gold did not directly test case sensitivity; and our interval gold did not test integer-subclass endpoints.

I should have caught that before running the study. Passing executable checks did not establish that our examples met our full rubric.

## What changes in the conclusion

Report 002's “none met every requirement” remains an accurate description of the recorded rubric decisions. It should not be read as a clean, independently validated measurement that Qwenny failed at everything, or that fine-tuning cannot help.

The factual execution record still matters: all 24 answers finished, eight suites passed the correct implementation, and five met the existing three-defect credit rule. Wrong offsets, malformed tests and wrong arguments remain genuine observed errors. But our broader grading system needs repair before it can fairly support model selection.

A familiar analogy: an examination asks students to meet a standard that its own model answers do not meet. A zero on that examination cannot by itself tell us how capable the students are.

## What happens next

We will prioritize a CPU-only audit connecting four things:

| Item | Question |
|---|---|
| Instructions | What did we explicitly ask the model to do? |
| Gold answer | Does our example actually demonstrate those requirements? |
| Defective implementations | Can the tests detect meaningful violations? |
| Score | Does the measurement credit the right behavior fairly? |

Start with the eight study tasks, then extend to the 60 training and 12 development tasks. New coverage expectations must be explicit or reported separately from following the instructions. Revised examples and scoring belong in a new version.

The reviewer also suggests using the existing answers to study individual expected values. That could be useful without GPU work, but it needs a declared extraction/scoring method and must be labeled exploratory. We have not performed that rescoring yet.

## What stays preserved

S006, its original scores, candidate-006, models and raw answers stay unchanged. This correction is an addendum, not a rewritten history. Final and regression task contents remain reserved.

No further training or model generation ran while incorporating the review.

## A small glossary

- **Gold answer:** our authored example of a good answer; it must be checked rather than assumed correct or complete.
- **Rubric calibration:** checking that the grading rules work on answers whose strengths and weaknesses we understand.
- **Measurement validity:** whether a score measures what we claim it measures.
- **Post-hoc analysis:** an analysis designed after seeing results. It can teach us something, but needs that label.
- **Requirement traceability:** a visible link from an instruction to the example and check that demonstrate it.

[Full review and our response](../program/reviews/REVIEW_001_RESPONSE.md) · [Current state](../program/CURRENT_STATE.md)

