Function contract: rotate_right(values, steps).

- values: an exact tuple (arbitrary elements; reject tuple subclasses).

- steps: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

values must be an exact built-in tuple; elements may be arbitrary objects. Rotate right by signed steps, wrapping modulo length; negative steps rotate left. Empty input returns (). Preserve element identities and order; do not mutate elements.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import rotate_right'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
