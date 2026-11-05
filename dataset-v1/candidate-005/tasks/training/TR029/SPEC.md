Function contract: chunk_list(values, width).

- values: an exact list of exact ints (reject bool, subclasses and list subclasses).

- width: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require width > 0, otherwise ValueError. Return consecutive lists of at most width items; keep the final partial chunk. Empty input returns []. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import chunk_list'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
