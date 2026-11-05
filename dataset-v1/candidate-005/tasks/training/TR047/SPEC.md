Function contract: index_of_nth(text, needle, occurrence).

- text: an exact built-in str (reject subclasses).

- needle: an exact built-in str (reject subclasses).

- occurrence: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require nonempty needle and occurrence >= 1, otherwise ValueError. Return the start index of that occurrence, counting overlapping matches; return -1 if absent.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import index_of_nth'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
