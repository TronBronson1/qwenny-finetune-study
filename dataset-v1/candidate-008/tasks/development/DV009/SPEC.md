Function contract: lower_bound(values, target).

- values: exact list of exact ints; reject bool, int subclasses and list subclasses.

- target: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require values nondecreasing, otherwise ValueError. Return the first insertion position that keeps target before all equal values (bisect-left behavior).

Return type: exact built-in int.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty, before, equal, after, leftmost-duplicate, gap, negative. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare valid inputs before and after calls.

Write one complete pytest file importing 'from subject import lower_bound'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
