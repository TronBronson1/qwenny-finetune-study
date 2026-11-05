Function contract: parity_label(number).

- number: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return exactly 'even' for an even integer, otherwise 'odd'. Negative integers follow the same rule.

Return type: exact built-in str.

Coverage expectations: include normal cases for zero, odd, even, negative-odd, negative-even, large. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import parity_label'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
