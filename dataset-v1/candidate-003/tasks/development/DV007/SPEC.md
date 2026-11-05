Function contract: grid_neighbors(row, column, rows, columns).

- row: an exact built-in int (reject bool and subclasses).

- column: an exact built-in int (reject bool and subclasses).

- rows: an exact built-in int (reject bool and subclasses).

- columns: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require positive rows/columns, otherwise ValueError; then require an in-bounds cell, otherwise IndexError. Return in-bounds orthogonal neighbor (row,column) tuples in up, right, down, left order. Do not include the original cell.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import grid_neighbors'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
