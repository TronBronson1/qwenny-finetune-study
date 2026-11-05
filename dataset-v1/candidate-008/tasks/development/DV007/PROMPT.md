Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution.

Function contract: grid_neighbors(row, column, rows, columns).

- row: exact built-in int; reject bool and int subclasses.

- column: exact built-in int; reject bool and int subclasses.

- rows: exact built-in int; reject bool and int subclasses.

- columns: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require positive rows/columns, otherwise ValueError; then require an in-bounds cell, otherwise IndexError. Return in-bounds orthogonal neighbor (row,column) tuples in up, right, down, left order. Do not include the original cell.

Return type: exact built-in list of exact two-item tuples of exact built-in ints.

Coverage expectations: include normal cases for single-cell, top-left, interior-order, bottom-right, single-row, single-column. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import grid_neighbors'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
