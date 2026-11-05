Function contract: parenthesis_depth(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Only '(' and ')' are permitted. Require a balanced sequence with no premature closing parenthesis, otherwise ValueError. Return maximum nesting depth as int; empty input returns 0.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parenthesis_depth'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
