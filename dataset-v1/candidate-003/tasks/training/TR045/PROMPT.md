Function contract: path_segments(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Split on literal '/' and discard empty segments only. Preserve '.', '..', backslashes, spaces and all other characters; this is not path normalization.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import path_segments'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
