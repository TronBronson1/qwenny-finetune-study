Function contract: remove_at(values, index).

- values: an exact list of exact ints (reject bool, subclasses and list subclasses).

- index: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 0 <= index < len(values), otherwise IndexError (negative indices are forbidden). Return a new list with exactly that item removed. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import remove_at'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
