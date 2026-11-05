# S006 execution protocol — run s006-001
Declared November 4, 2026 (America/New_York), before generation. This execution specification resolves the draft in PROTOCOL.md. It is effective only together with freeze-manifest.json and passed preflight.json.

## Question and arms
Explore familiar-example construction versus transfer and completion. Frozen NF4 base versus original qwenny-001 E1 and E5, one first attempt per task/arm, seed42 reset each cell. No optimizer updates. E1 inclusion is motivated by earlier development evidence; this is exploratory.

## Fixed selection
Use selection.json rule and inputs. Four training tasks: TR024 ASCII upper, TR025 run-length encode, TR038 hex byte, TR049 row-major offset.
Four development tasks: DV008 edit distance, DV004 XOR checksum, DV011 interval union, DV007 grid neighbors.
Choose lowest-ID representative per family, order by supplied target length then ID, and choose indices 0, floor((n-1)/3), floor(2*(n-1)/3), n-1 independently per split. Exclude DV001/DV002. No output-based selection; no category-balance or population-representativeness claim.
Alternate training/development tasks in their selected order. Rotate base/E1/E5 arm order by task index.

## Inputs and inference
Instruction-only direct-answer messages; training inputs exactly match original approved corpus system/user messages. Development uses original request packets. All 12 development targets previously contributed loss measurements. Render and save prompts/token IDs before generation; use identical saved inputs across arms.
Pinned base revision c202236235762e1c871ad0ccb60c8ee5ba337b9a and existing NF4/BF16 CPU-embedding runtime. Exact E1/E5 reload probe equality required.
Thinking disabled; temperature1/top_k20/top_p.95; presence0/repetition1; max_new_tokens2048; context ceiling16134 without prompt truncation. Explicit im_end248046/endoftext248044 stops. No cap increases, repairs, retries, best-of-N, or failed-answer training targets.
Save raw text, generated token IDs, progress/partial text, extraction, prompt hashes, times, stop reasons, memory and source snapshots.

## Resource limits
Local RTX3080; existing runtime requires >=8GiB free before load. No app closure or cloud. Single GPU owner. Per-cell 1200 seconds and total model-preflight/generation 10800 seconds checked at token boundaries. Initial file verification/model loading are not interruptible by this soft boundary, so document any overshoot. Unexpected exceptions/probe mismatch/OOM stop the run; preserve all artifacts. Wall-time-stopped output is incomplete. No automatic rescue or restart.
Scoring uses Python3.15/pytest9.2, isolated per candidate/implementation, plugin autoload disabled, 20-second subprocess timeout. GPU generation and CPU scoring/reporting costs reported separately.

## Frozen acceptance and report
COVERAGE_RUBRIC.json defines common and task-specific review before outputs exist. Require complete format, nontruncated answer, reference validity, all three relevant designated mutant detections, complete applicable contract coverage, and honest mapping/limitations.
Read/hash-bind source before execution; no reasoning-only code harvesting. Only approved safe files enter isolated evaluation. A syntax-invalid file may be recorded as a collection failure without repair; unsafe code is excluded explicitly. Reference-invalid files receive no eligible mutant score.
Report all cells and separate denominators for training and development, plus completion, parse/collection, reference, mutant and coverage layers. No general aptitude claim or checkpoint selection from this one-seed study.

## Decision branches and boundaries
Use the interpretation branches in the original draft; no outcome automatically authorizes more training. Better familiar-task scores do not prove transfer; poor development scores do not identify a mechanism. No final/regression task access or claims of LM Studio deployment validation.
The original adoption question still requires a frozen strong-prompt baseline and final/regression evaluation later.

