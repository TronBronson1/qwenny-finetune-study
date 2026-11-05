Function contract: int_to_base(number, base).

- number: an exact built-in int (reject bool and subclasses).

- base: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require number >= 0 and 2 <= base <= 16, otherwise ValueError. Return the lowercase positional representation without leading zeros, except zero is '0'. Digits above 9 are a through f.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import int_to_base'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
