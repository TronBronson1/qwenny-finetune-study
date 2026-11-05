Function contract: wrap_index(index, length).

- index: an exact built-in int (reject bool and subclasses).

- length: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require length > 0, otherwise ValueError. Return the canonical wrapped index in range(length), including for negative indices.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import wrap_index'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
