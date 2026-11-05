# Qwenny observations and questions for later study

## 2026-11-04 — user experience and experiment boundary

User instruction: keep the current experiment unchanged at this stage. Record
additional abnormalities and parameters worth studying. This note does not change
the protocol, scores, candidate selection, or authorization for further runs.
Preserve all existing results and keep final-test/regression families untouched.

### User-reported observations

- In the user's experience, Qwenny spends much more context on thinking than on
  the final answer.
- The user has observed significantly less thinking and erratic/repetitive behavior
  (described as "spazzing") on algorithm and coding tasks.
- These are qualitative observations from the user's workflow, not measurements
  from a matched task-category comparison. Exact prompts/settings for these
  observations are not newly established here.

### Observations from the completed thinking-001 run

- Five of six first attempts reached the declared 8192-new-token cap. Three never
  closed thinking. For the three that did close, tokens before/after the delimiter
  were 7246/945 (base rotation), 6461/442 (original E5 rotation), and 7829/362
  (base clock). After-close counts include a stop token where present.
- Saved output tails show repeated checking/repetition of instructions in unfinished
  thinking. This records visible behavior; its cause is not established.
- The tasks requested pytest generation from contracts. They do not represent a
  broad sample of algorithm implementation or ordinary coding tasks, so the run
  does not contradict or verify the user's task-category observation.
- The run allowed 8192 generated tokens inside a configured 16134-token context.
  The generation cap was an experimental choice, not an established hardware or
  model limit. Full-context behavior remains unmeasured in this Python setup.
- GPU-wide sampled free memory fell to 68 MiB. Per-process shared-memory counters
  were unavailable. Memory spill and the cause of the first attempt's slowdown
  remain unverified.

### Parameters/questions to register for a future, separate protocol

- Task category: algorithm implementation, ordinary coding, and contract-based
  test generation. Measure reasoning length, final-answer length, repetition,
  completion, and correctness separately on development-only tasks.
- Total context versus generation budget: record prompt occupancy, thinking
  closure, and remaining answer space. Do not extend or rescue thinking-001.
- Decoding controls: presence penalty, sampling settings, and seed. The local
  thinking control used presence0; historical LM Studio used presence1.5.
- Runtime/model representation: pinned NF4 Python base/adapters versus historical
  GGUF/LM Studio. Deployment lineage remains unresolved; no precision cause inferred.
- Direct-answer training versus thinking-enabled inference, including whether
  instruction-checking repetition differs between base and adapters.
- Memory placement and context scaling after the planned RAM upgrade. More system
  RAM does not automatically enlarge GPU memory or change the current configuration.

Change one factor at a time where feasible, declare any follow-up before running,
and retain first attempts. None of these questions establishes a diagnosis or
justifies changing the completed experiment, training on failed development
outputs, selecting a winner, or accessing final-test tasks.

Existing result and handoff: training-v1/THINKING_CONTROL_RESULTS.md and
HANDOFF_THINKING_CONTROL.md. This is a supplementary note; those artifacts and
their recorded hashes remain unchanged.
