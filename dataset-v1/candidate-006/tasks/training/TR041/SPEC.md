Function contract: parse_int_pair(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require two comma-separated signed canonical decimal integers. Each component is at most 12 digits excluding an optional minus; '-0' is permitted. No plus, whitespace or leading zeros except 0. Invalid syntax raises ValueError. Return a tuple of two ints.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_int_pair'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
