Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution.

Function contract: rotate_right(values, steps).

- values: exact tuple of arbitrary objects; reject tuple subclasses.

- steps: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

values must be an exact built-in tuple; elements may be arbitrary objects. Rotate right by signed steps, wrapping modulo length; negative steps rotate left. Empty input returns (). Preserve element identities and order; do not mutate elements.

Return type: exact built-in tuple containing the original element objects, preserving their identities.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty-zero, empty-positive, single-negative, identity, right, left, wrap, duplicates, mutable-elements. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare inputs before and after every call, including calls that raise. Compare arbitrary element objects by identity, not by copied value.

Write one complete pytest file importing 'from subject import rotate_right'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
