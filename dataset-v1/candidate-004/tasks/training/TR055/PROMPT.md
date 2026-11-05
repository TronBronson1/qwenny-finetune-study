Function contract: encode_rgb(red, green, blue).

- red: an exact built-in int (reject bool and subclasses).

- green: an exact built-in int (reject bool and subclasses).

- blue: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require every component in 0..255, otherwise ValueError. Return exactly seven characters '#rrggbb' using lowercase hexadecimal.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import encode_rgb'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
