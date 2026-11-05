Function contract: format_cents(cents).

- cents: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return exact decimal currency units with two fractional digits and no grouping/currency symbol. Negative amounts have one leading minus. Avoid floating point; zero is '0.00'.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import format_cents'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
