Function contract: common_prefix(left, right).

- left: an exact built-in str (reject subclasses).

- right: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return the longest literal, case-sensitive common prefix of two strings.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import common_prefix'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
