Function contract: interleave_strings(left, right).

- left: an exact built-in str (reject subclasses).

- right: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Alternate one character from left, then one from right. Append the remainder when one ends. Do not discard whitespace or Unicode.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import interleave_strings'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
