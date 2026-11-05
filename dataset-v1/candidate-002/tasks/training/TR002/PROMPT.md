Function contract: strip_prefix(text, prefix).

- text: an exact built-in str (reject subclasses).

- prefix: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

prefix must be nonempty, otherwise ValueError. Remove exactly one case-sensitive literal prefix if present at the start. Preserve whitespace and Unicode; empty text is valid.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import strip_prefix'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
