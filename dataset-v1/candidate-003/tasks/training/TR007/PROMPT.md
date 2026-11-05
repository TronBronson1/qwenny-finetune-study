Function contract: digit_sum(number).

- number: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require number >= 0, otherwise ValueError. Return the sum of its decimal digits; zero returns zero.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import digit_sum'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
