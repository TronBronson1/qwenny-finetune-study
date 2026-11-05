Function contract: wrap_index(index, length).

- index: exact built-in int; reject bool and int subclasses.

- length: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require length > 0, otherwise ValueError. Return the canonical wrapped index in range(length), including for negative indices.

Return type: exact built-in int.

Coverage expectations: include normal cases for unit-length, positive-wrap, negative-one, negative-period, positive-period, large. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import wrap_index'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
