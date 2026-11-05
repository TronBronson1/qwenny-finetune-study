# What the likelihood measurement does and does not say

Teacher forcing asks: given the prompt and every preceding correct reference
token, how plausible is the next reference token? Free generation supplies the
model's own preceding choices. A plausible alternative input, identifier or case
count can put it on a continuation that was not measured by the reference loss.
Any such divergence is not inherently an error; executable contract checks are
needed to distinguish alternatives from incorrect answers.

The existing aggregate loss is token-weighted within each answer. Repeated
boilerplate and prose can dominate its reduction, while one incorrect expected
value can invalidate an otherwise plausible pytest file. An average token score
also cannot establish completeness of contract coverage or reliable stopping.

These mechanisms are consistent with the current measurements and observed
outputs. They are not proof of a single causal explanation. This experiment does
not isolate 4-bit precision, cache behavior over all generated histories,
training-data breadth, optimizer settings or thinking-enabled inference.

Recommended subsequent ablation: compact the training target format while
preserving every training case and assertion, then compare against the current
format with the same base revision, split, training examples, optimizer updates,
adapter scope and predeclared development decoder. Keep the current reference
targets and checkpoints intact; use a separately versioned target export.
Report any token-count/batching differences rather than calling the runs
compute-matched. Evaluate syntax, reference validity, designated mutants,
coverage, completion and length separately from loss. Do not train on the failed
development outputs or edit development cases to help a candidate.

A thinking-enabled matched base/adapted generation comparison remains a separate
useful control before drawing conclusions about the original LM Studio workflow.
