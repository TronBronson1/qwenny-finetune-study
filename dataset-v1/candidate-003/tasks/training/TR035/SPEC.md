Function contract: adjacent_equal_count(values).

- values: an exact list of exact ints (reject bool, subclasses and list subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return how many adjacent pairs are equal. Runs of length k contribute k-1; empty or one item returns 0. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import adjacent_equal_count'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
