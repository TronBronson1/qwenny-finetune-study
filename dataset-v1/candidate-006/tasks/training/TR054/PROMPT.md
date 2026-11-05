Function contract: grouped_decimal(number).

- number: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return decimal integer text grouped from the right in groups of three with underscores. Preserve a leading minus, never add plus or leading zeros.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import grouped_decimal'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
