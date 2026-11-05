Function contract: transpose(matrix).

- matrix: an exact list of exact lists of exact ints (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require a rectangular list of lists, otherwise ValueError. Return its transpose as lists. [] and any rectangular matrix with zero columns transpose to []. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import transpose'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
