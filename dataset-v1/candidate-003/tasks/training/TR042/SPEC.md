Function contract: parse_version(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require exactly three dot-separated canonical nonnegative decimal components, each 0 through 999. No leading zeros except '0', signs, whitespace or Unicode digits. Invalid syntax raises ValueError. Return a tuple of three ints.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_version'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
