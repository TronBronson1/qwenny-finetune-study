Function contract: unravel_index(index, rows, columns).

- index: an exact built-in int (reject bool and subclasses).

- rows: an exact built-in int (reject bool and subclasses).

- columns: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require rows > 0 and columns > 0, otherwise ValueError. Then require 0 <= index < rows*columns, otherwise IndexError. Return (row,column) in row-major order.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import unravel_index'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
