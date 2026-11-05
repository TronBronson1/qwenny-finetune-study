Function contract: plural_count(number, noun).

- number: an exact built-in int (reject bool and subclasses).

- noun: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require number >= 0 and nonempty noun, otherwise ValueError. Return '<number> <noun>' for 1, and append exactly 's' to noun otherwise. This is literal formatting, not English inflection.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import plural_count'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
