# Latest Qwenny handoff: likelihood versus generation gap

2026-11-03 local time. Read HANDOFF_TRAINED_QWENNYS.md for checkpoint, environment,
dataset provenance, authorization and model-deployment details. Those remain valid.

The user requested investigation of target likelihood versus free-running
correctness. Completed locally without optimizer updates, target changes, final
test access, cloud use or LM Studio changes. All GPU work has finished.

Primary report: training-v1/investigations/gap-001/README.md.
Machine results: that folder's RESULTS.json; exact methodology METHOD.md;
recommendations INTERPRETATION.md. Eight new outputs and four unchanged original
outputs compare base/E5, instruction-only prompts, thinking off, output cap2048,
seed42, greedy presence0, sampled presence0 and original sampled presence1.5.
The presence penalty is custom output-only, not asserted identical to LM Studio.

All six model/decoder cells scored 0/2 strict acceptance. Of eight new outputs:
three truncate without complete code, four complete files fail the correct
implementation, one complete file has a syntax error. Full source reviewed before
hash-bound isolated pytest execution; original references/3 mutants untouched.
New scoring and definitive rejection reasons: training-v1/scoring/gap-001.

Teacher-forced NLL reproduces saved run measurements within .005. Rotation base
.9278 -> E5 .3152; clock .7862 -> .0996. E5 reference-next-token top1 accuracy
92.7%/98.0% under correct histories. This is NOT program correctness. Prose plus
broad other-code spans account for 97.1%/87.7% of NLL reduction; other code includes
semantic assertions and is not pure formatting. Rotation expected-value NLL does
not improve. Clock's residual uncertainty concentrates in constructing inputs.
Presence penalty's correct-history NLL effect is small/mixed, and removing it
does not repair these first attempts. Greedy E5 outputs both truncate by excessive
enumeration/repetition; no arbitrary cap increase or rescue was applied.

Interpretation: learned continuation structure does not establish autonomous
contract-correct generation, good case selection or stopping. Evidence is two
visible development families/one seed; no general aptitude or quantization blame.
No causal exclusion of long-cache, training breadth, optimizer or thinking mode.

Next proposed work: prepare a separately versioned compact-target format with
the same substantive training cases/assertions; hold base/split/optimizer updates/
adapter scope fixed and record token/batching differences. Predeclare development
decoder and score execution, coverage, completion and length separately from NLL.
A matched thinking-enabled base/adapted control is also still outstanding before
claims about the historical LM Studio workflow. Neither follow-up has started.
Never use failed development outputs as training targets, modify frozen scoring
to help a candidate, discard first attempts, or touch final families early.
