Function contract: bounded_slice(values, start, stop).

- values: an exact list of exact ints (reject bool, subclasses and list subclasses).

- start: an exact built-in int (reject bool and subclasses).

- stop: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 0 <= start <= len(values) and 0 <= stop <= len(values), otherwise IndexError. Return the half-open slice; start > stop returns []. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import bounded_slice'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
