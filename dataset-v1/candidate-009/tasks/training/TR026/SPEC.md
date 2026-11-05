Function contract: stable_unique(values).

- values: exact list of exact ints; reject bool, int subclasses and list subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return first occurrences only, preserving input order.

Return type: exact built-in list of exact built-in ints.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty, single, stable-order, zero-negative, already-unique. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare inputs before and after every call, including calls that raise.

Write one complete pytest file importing 'from subject import stable_unique'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
