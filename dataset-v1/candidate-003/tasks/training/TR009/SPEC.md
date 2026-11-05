Function contract: signed_gcd(left, right).

- left: an exact built-in int (reject bool and subclasses).

- right: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return the nonnegative greatest common divisor. gcd(0,0) is 0; input signs do not affect the result.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import signed_gcd'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
