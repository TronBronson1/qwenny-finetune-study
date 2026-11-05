# Study register
Updated November 4, 2026. IDs below are retrospective navigation labels; original run IDs and dates remain authoritative. These studies were not all preregistered under these labels.

| ID | Question | Status / finding | Evidence |
|---|---|---|---|
| S001 | Do demonstrations help in the initial workflow? | Complete; two-task pilot showed no first-attempt benefit. | [Prompt comparison](../prompt-comparison/COMPARISON_RESULTS.md) |
| S002 | Can local training run and produce verified adapters? | Complete; feasibility and training established, quality gain not established. | [2048 fit](../lora-feasibility/FIT_2048_RESULTS.md), [training plan](../training-v1/PLAN.md), [training results](../training-v1/RESULTS.json) |
| S003 | Does changing decoding explain the likelihood/generation gap? | Complete; tested changes did not yield strict accepted answers. | [Gap investigation](../training-v1/investigations/gap-001/README.md) |
| S004 | Does a shorter target presentation improve output? | Complete; compact E5 pilot 0/2, both syntax-invalid. | [Compact trial](../training-v1/COMPACT_TRIAL_RESULTS.md) |
| S005 | Does bounded thinking-enabled inference help? | Complete; all three arms 0/2. | [Thinking control](../training-v1/THINKING_CONTROL_RESULTS.md) |
| S006 | Is failure already present on familiar examples, or does it emerge on transfer/completion? | Complete: all 24 answers finished; 8 reference-valid, 5 met all-three-mutant rule, 0 strict accepted. Failures also on familiar tasks. Self-reviewed, not independently validated. | [Results](../studies/S006-learning-and-transfer/RESULTS.md), [interpretation](../studies/S006-learning-and-transfer/INTERPRETATION.md) |
| S007 | Can gold/prompt/rubric alignment and requirement-linked fixtures be repaired? | Complete: 72 reference suites / 1475 cases and 407 mutants pass calibration; five negative controls rejected. Fit overlay validated, no training. | [Results](../studies/S007-measurement-repair/RESULTS.md) |
| S008 | Can existing models calculate supplied return values without writing tests? | Complete: base 22/32, E1 23/32, E5 22/32; one E5 response unscorable. No winner selected. | [Results](../studies/S008-fixed-input-values/RESULTS.md), [interpretation](../studies/S008-fixed-input-values/INTERPRETATION.md) |
| S009 | Do verified calculation comments improve matched fresh calibrated training? | Ended incomplete: prep/scorer/both GPU preflights passed; baseline stopped at 1200s after 213 logged examples / 53 updates. No comment training, E5 or scored attempts; quality unmeasured. | [Results](../studies/S009-value-comments/RESULTS.md), [Report 006](../observer/REPORT_006.md) |

Historical 0/2 results belong to specific settings and tasks; do not pool them into an overall accuracy estimate.

Review addendum: S006's strict counts are not calibrated capability estimates. Independent review identified gold/rubric inconsistencies, with three examples directly confirmed. Original records remain unchanged; [review disposition](reviews/REVIEW_001_RESPONSE.md) qualifies their interpretation.

