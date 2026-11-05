Function contract: parse_range(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require literal syntax '[low:high]' with canonical ASCII decimal endpoints 0 through 99 and low <= high. No spaces/signs/leading zeros except 0. Invalid input raises ValueError. Return the endpoint tuple.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_range'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
