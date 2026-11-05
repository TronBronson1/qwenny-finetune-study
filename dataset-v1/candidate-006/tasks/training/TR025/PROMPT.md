Function contract: run_length_encode(values).

- values: an exact list of exact strings (reject subclasses at both levels).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return a list of (string, run_length) tuples for consecutive equal strings. Empty input returns []; do not combine separated runs.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import run_length_encode'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
