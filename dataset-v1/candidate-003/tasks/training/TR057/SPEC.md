Function contract: make_slug(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Only ASCII letters, digits, space, hyphen and underscore are permitted; other characters raise ValueError. Treat space/hyphen/underscore runs as separators, lowercase letters and join nonempty parts by one hyphen. All-separator input returns ''.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import make_slug'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
