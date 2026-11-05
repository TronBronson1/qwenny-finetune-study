Function contract: compare_versions(left, right).

- left: an exact tuple of exactly three exact ints.

- right: an exact tuple of exactly three exact ints.

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Each argument must have exactly three nonnegative integer components, otherwise ValueError. Compare lexicographically and return exact int -1, 0, or 1.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import compare_versions'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
