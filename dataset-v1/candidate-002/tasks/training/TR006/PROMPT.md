Function contract: factorial(number).

- number: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 0 <= number <= 12, otherwise ValueError. Return number factorial as an integer; 0! is 1.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import factorial'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
