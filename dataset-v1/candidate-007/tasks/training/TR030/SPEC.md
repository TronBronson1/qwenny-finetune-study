Function contract: transpose(matrix).

- matrix: exact list of exact lists of exact ints; reject bool and subclasses at all stated levels.

Reject invalid specified types with TypeError before shape/value checks.

Require a rectangular list of lists, otherwise ValueError. Return its transpose as lists. [] and any rectangular matrix with zero columns transpose to [].

Return type: exact built-in list of exact built-in lists of exact built-in ints.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty, one-zero-column, several-zero-columns, square, one-row, one-column. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare valid inputs before and after calls.

Write one complete pytest file importing 'from subject import transpose'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
