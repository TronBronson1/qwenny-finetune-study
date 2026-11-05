Function contract: parity_label(number).

- number: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return exactly 'even' for an even integer, otherwise 'odd'. Negative integers follow the same rule.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parity_label'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
