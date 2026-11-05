Function contract: is_square(number).

- number: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require number >= 0, otherwise ValueError. Return an exact bool indicating whether number is a perfect square.

Return type: exact built-in bool.

Coverage expectations: include normal cases for zero, one, nonsquare, square, below-square, square-sixteen, above-square, large-square. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import is_square'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
