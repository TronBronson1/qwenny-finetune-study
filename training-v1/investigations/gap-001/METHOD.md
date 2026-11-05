# Likelihood versus free-running correctness: gap-001

Development-only investigation. No optimizer, weight updates, target edits,
prompt repairs, retries, cloud uploads or final-test access.

Compare frozen base and epoch-5 on DV001 rotation and DV002 clock using identical
instruction-only messages. New first attempts: greedy with presence penalty zero
and sampling with presence penalty zero. Reuse original sampling/presence-1.5
first attempts from probes/qwenny-001-direct-001 (base-A and epoch-5-C).
This is three decoder conditions, not a full factorial experiment. Sampling:
seed 42, temperature 1, top-k 20, top-p .95; all runs thinking disabled,
2,048 new-token cap, context 16,134, explicit im_end/endoftext stops.
The earlier penalty subtracts 1.5 once for each token seen anywhere in generated
output; it is not asserted equivalent to LM Studio's implementation.

Teacher-forced diagnostics supply the correct preceding reference tokens. Their
unpenalized NLL must reproduce the saved training-run development measurement
within .005. AST/source spans partition supervised reference tokens into test
inputs, expected values, exception classes, exact-type assertions, other code and
mapping/prose. These are approximate lexical regions, not semantic labels.
In particular, 'other code' includes assertions and executable logic.

Also measure applying the pilot penalty and top-k/top-p filtering on those same
correct histories. A target excluded by filtering means only that this one
reference token is unavailable at this history. A different token can form an
equally valid answer. Teacher-forced token accuracy is not program correctness,
and none of these quantities are a probability that an entire free-running
answer is correct.

Review each complete code block before hash-bound isolated pytest execution.
Use unchanged correct implementations and three designated mutants per family.
Require reference validity before crediting mutant detections. Review contract
coverage and answer prose separately; three mutant detections alone do not
establish strict acceptance. Preserve truncations as failures under this cap.

Limits: two previously visible development families, one sampling seed, direct
answers only. No causal precision comparison, general aptitude ranking, broad
regression result, thinking-enabled comparison or deployment claim is implied.
This investigation does not establish whether longer output limits would help.
