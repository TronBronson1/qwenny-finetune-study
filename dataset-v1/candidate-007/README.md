# Candidate 007 — calibrated repair, not a training export

60 training and 12 development tasks only. Final/regression tasks are omitted and the original candidate-006 remains intact.

All 72 revised gold suites passed the correct references (1,475 cases) and rejected all 407 designated mutants through declared witnesses. Five negative controls were correctly rejected. See ../../studies/S007-measurement-repair/calibration-certificate.json and validation-002/summary.json.

The correct implementations are unchanged. Rubric mappings and instruction wording are explicit; this is finite same-agent calibration, not independent proof of exhaustive correctness. All source examples and fixtures remain inspectable.

No training approval/export is inherited from the old corpus hash, and no optimizer run used this candidate. One full training chat exceeds the previous 2,048-token fit; see the external token profile before training. Current approved historical exports and CURRENT_CANDIDATE.txt remain unchanged.

build-sources preserves the original repair builder and config. finalize_metadata.py is the separate post-validation metadata normalization step. Initial authoring hashes and the code-identical validation binding are preserved outside this snapshot.
