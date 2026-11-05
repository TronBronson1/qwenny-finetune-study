# S006 — Learning, transfer, and completion diagnostic
Status: DRAFT, November 4, 2026. No generation or training has occurred under this proposal.

Execution update: this draft is retained as design history. The resolved [frozen protocol](PROTOCOL_FROZEN.md), passed preflight.json, and freeze-manifest.json govern run s006-001, authorized by the user after reviewing the program documents. Consult the program current state for live status.

## Question
Can original adapters produce valid tests on familiar training specifications under a bounded matched inference protocol, and how does that behavior compare with development specifications?

## Why now
Training/import integrity checks passed and teacher-forced loss fell, but strict free-generation acceptance did not improve in small pilots. The next intervention depends on whether failure already appears on familiar examples, transfers poorly, or mainly concerns completion.

## Proposed design
No optimizer updates. Compare pinned NF4 base, original E1, and original E5. E1 is included because the original clock near-pass makes endpoint-only comparisons incomplete; this is a motivated exploratory choice, not a prospectively discovered winner.

Use a small training subset and development subset. Choose exact IDs using a reproducible selection rule fixed before inspecting new answers, with family deduplication and length/category balance based only on declared metadata. Record why the subset is manageable and what it excludes. Do not read final or regression content.
All development targets already contributed teacher-forced loss. Training results measure familiar-example performance; development generation measures exploratory transfer, not pristine held-out performance.

Default proposal for review: 4 training families and 4 development families, 3 arms, seed42, 24 first attempts, instruction-only direct answers. Thinking disabled to inspect answer construction without spending the budget on reasoning. Sampling temperature1/top_k20/top_p.95, presence0/repetition1, cap2048, context16134, verified im_end/endoftext stops. These intentionally match the existing direct sample0 condition. No comparison may attribute differences from thinking-001 solely to thinking because its budget differs.
If profiling shows this budget excludes supplied complete targets for selected tasks, amend the design before freeze; never lengthen a scored attempt after observing failure.

## Must resolve before freeze
- Exact task IDs, metadata selection rule, and family overlap/exposure audit.
- Exact saved model messages and their relationship to approved training messages; document any mismatches.
- Exact base/checkpoint/probe hashes and code/environment versions.
- Rotated arm order, seed handling and target/token fit per arm.
- Predeclared total wall-time budget based on existing throughput records, memory boundary, and interruption behavior.
- Scoring rubric for each task's explicit requirements, frozen before seeing new outputs.
- Reviewer assignment and resolution of material concerns.
- Authorization scope for the actual local execution.

## Measurements
Report each cell: completion/stop reason; reasoning/final separation where relevant; tokens and elapsed time; parse/collection status; reference-valid suite; relevant kills of frozen designated mutants (eligible only when reference-valid); explicit requirement coverage; strict acceptance; unsupported execution claims.
Keep source outputs unchanged. Review/hash-bind generated source before isolated execution. Never execute incomplete source repaired by the evaluator. Separate infrastructure errors from model failures.
Report counts separately for familiar training and development tasks. One seed is exploratory; do not estimate general aptitude or treat three arms as independent task samples.

## Interpretation branches
- Training passes, development fails: consistent with limited transfer; investigate data diversity and contract construction. Not proof of memorization or its mechanism.
- Both fail: investigate training/inference alignment and error categories before choosing more training.
- Reference-valid but coverage-invalid: investigate specification coverage and evaluator rubric; do not lower strict acceptance.
- Widespread truncation: justify a new completion-focused study; do not repair this study by raising caps.
- All poor or ambiguous: report the bounded negative finding; consider stopping or redesigning rather than automatically expanding compute.
- E1 exceeds E5: exploratory checkpoint evidence only; confirm prospectively before selection.
- Better results across arms: determine whether the changed task mix explains them before attributing improvement to adapters.

## Reserved boundaries
No final/regression access, best-of-N, repairs, failed-output training targets, cloud, deployment changes, or new training. Final practical comparison must eventually include the strong prompted baseline (arm B); this diagnostic does not answer that original adoption question.

