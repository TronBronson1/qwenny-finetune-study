# S008 interpretation

Completed November 4, 2026. Existing base/E1/E5 only; no new training.

All 24 greedy first attempts finished normally. Base scored 22/32 supplied values, E1 23/32 and E5 22/32. Each model answered all four values correctly on three of eight tasks. Typed JSON accuracy matched value accuracy on scorable correct cases. E5/TR025 was not valid JSON: it returned (str,int) schema placeholders rather than concrete return values; that response contributes zero out of four under the frozen rule and is reported as unscorable, not four demonstrated arithmetic errors.

## Observations

- All three models handle the selected ASCII-uppercase and hexadecimal cases correctly.
- Base/E1 also answer all four run-length cases correctly; E5's run-length response has a format/schema failure.
- E5 answers all four row-major offsets correctly; base answers one and E1 two. This is a concrete task-specific observation, not a general ranking.
- All three predict 0 for the last XOR case, whose correct output is 1 after duplicate 128 cancellation.
- All three fail the literal Unicode-representation edit case: U+00E9 versus U+0065 U+0301 has code-point Levenshtein distance 2, not 0.
- Interval-union and grid-neighbor results remain unreliable even with supplied inputs; E5 gets one more grid case right than base/E1, but not the full task.

These errors show that pytest syntax and self-selected test construction are not the only issues in this diagnostic. They do not prove the cause, establish universal inability to calculate, or imply that training on comments will fix them.

The Unicode case is visually easy to confuse: Python repr displays the combining character literally rather than as an escape. Future protocols should explicitly distinguish code points from normalized graphemes and may test representation clarity prospectively. Preserve this case and its original expected result; do not revise or retry the response.

## Limits

Same eight visible purposive tasks, one greedy condition, four supplied cases per task. The primary denominator includes parsing/format failures as zero, with separate parse metrics. Cases within a task/response are dependent; these counts are descriptive, not independent population samples.

The supplied cases, contract presentation, response format, decoder and budget differ from S006. No single-factor causal comparison with S006 is justified. No demonstration baseline or final/regression evaluation occurred. The adapters were trained on candidate-006, not the repaired corpus.

## Decision

No winner or deployable upgrade selected. Preserve all candidates. Next training work should be a separately controlled value-focused target intervention on the calibrated, length-checked data, with a matched baseline and unchanged hardware/optimizer budget; do not simply add epochs.

Before any such run, finish an approved export/provenance record, exact assistant masking, token decode checks and an actual longest-example forward/backward. The presentation overlay must be explicit. A practical improvement claim ultimately still requires full executable-suite evaluation against a strong prompted base and a frozen held-out protocol.

The current batch ends after measurement repair, fit-preview validation and this fixed-input diagnostic; no automatic additional training is triggered.

