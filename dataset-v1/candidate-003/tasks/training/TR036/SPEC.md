Function contract: lower_median(values).

- values: an exact list of exact ints (reject bool, subclasses and list subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require nonempty input, otherwise ValueError. Return sorted position (len(values)-1)//2, so even lengths choose the lower middle. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import lower_median'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
