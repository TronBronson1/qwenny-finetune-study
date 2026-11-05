Function contract: partition_sign(values).

- values: exact list of exact ints; reject bool, int subclasses and list subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return a tuple (negatives, zeros, positives), each a list preserving original order.

Return type: exact built-in three-item tuple of exact lists of exact ints.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty, zero, all-signs-stable, positive-only, negative-only, positive-negative-order. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare valid inputs before and after calls.

Write one complete pytest file importing 'from subject import partition_sign'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
