Function contract: parse_hex_byte(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require exactly two ASCII hexadecimal digits, case-insensitive; otherwise ValueError. Return the byte value as int.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_hex_byte'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
