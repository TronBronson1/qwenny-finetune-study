# Gold/rubric behavioral follow-up

Received and replayed November 4, 2026. User-supplied external review, corroborated by local CPU replay. This is not independent validation of every mutant's single-defect semantics.

## Evidence preserved

external-evidence/ contains the five supplied checker/result files and available Python source copies from the scratchpad mutant experiments. external-evidence-sha256.json fingerprints all 38 archived source files. Raw structural flags, including false positives, remain visible.

replay_safe.py preserves the inspected reviewer experiment logic but replaces deletion of prior working directories with refusal to overwrite. It ran only the eight declared training/development cases under this directory, using established Python3.15/pytest9.2. No original corpus or study artifact was modified.

rubric_mutants.json and replay.log record all eight paired reference/broken-copy gold runs. Every reference and broken-copy suite passed. verify_witnesses.py and behavior-witnesses.json separately confirm a concrete reference-versus-mutant difference for all eight.

## Corroborated behavioral gaps

| Task | Split | Violated behavior that survives the gold suite |
|---|---|---|
| TR038 | Training | Non-ASCII hexadecimal digits accepted |
| TR043 | Training | Non-ASCII binary digits accepted |
| TR044 | Training | Non-ASCII decimal range endpoints accepted |
| TR056 | Training | Non-ASCII hexadecimal RGB digits accepted |
| DV010 | Development | Non-ASCII RPN integer digits accepted |
| DV008 | Development | Case-insensitive comparison |
| DV011 | Development | Integer-subclass endpoints accepted |
| TR027 | Training | Ordinary non-int element accepted on a one-item input |

The first seven comprise four training and three development targets. Only training targets entered optimizer updates; the development targets did not. TR027 is a separate additional demonstrated training gap.

The supplied eight-task semantic assessment rates TR024/TR025/TR049 pass, TR038/DV008/DV011 fail, and DV004/DV007 borderline. Record those as the external review's assessments, not new automatic decisions from a keyword scan. Ordinary-type absence can be a real gap but structural absence alone is not a complete semantic assessment.

The 16-task ordinary-element claim has only one concrete broken-copy demonstration (TR027) in the supplied saved result JSON. Treat the remaining task-level behavioral confirmations as pending, not disproved. The other 64 training/development tasks still need task-specific semantic review; the 72-task structural scan does not complete that review.

The user's before/after 1775-file hash check is reported external provenance; we did not reproduce that particular inventory. We separately verify existing S006 result fingerprints and its frozen source manifest.

## E5/DV008 disposition

The frozen record has reference validity, all three designated mutant credits, valid prose, and one recorded coverage gap: case sensitivity. Its gold shares that gap. This makes rubric calibration consequential, not a cosmetic objection.

Do not retroactively award acceptance. Case-sensitive comparison is explicit in the contract: repair the gold and add a valid case-sensitivity mutant in a new candidate, rather than remove that behavior simply to permit a pass. A future rubric may separate instruction-following, semantic coverage, and overall acceptance, but must state the policy explicitly.

Any v2 assessment of already-seen S006 outputs is a declared post-hoc sensitivity analysis, even if its procedure is frozen before running it. It is not a prospective confirmation or a new first attempt. Report old and new definitions side by side, and do not presume E5/DV008 will pass whichever defensible v2 is selected.

## Next gate

- Prepare a separate repair candidate/packet; preserve candidate-006, S006 and existing approved exports.
- Add concrete requirement-to-gold-to-mutant traceability, not just keyword heuristics.
- Add the seven demonstrated behaviors plus TR027 to proposed mutant validation. Review each mutant's validity, equivalence and failure relevance before official promotion; these scratchpad copies are not official mutants yet.
- Validate revised gold on the correct reference and every designated mutant, with meaningful witnesses, and assess the gold against the same prompt/rubric as the model.
- Resolve borderline task cases and extend semantic review to the remaining 64 tasks.
- No new model generation or training until the measurement/data gate is resolved. A changed corpus needs its own provenance and authorization; old approval is not silently transferred.

No model answers were generated, repaired or rescored in this follow-up.

