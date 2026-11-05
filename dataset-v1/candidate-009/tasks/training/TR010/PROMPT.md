Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution.

Function contract: population_count(number).

- number: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require number >= 0, otherwise ValueError. Return the number of set bits in its binary representation.

Return type: exact built-in int.

Coverage expectations: include normal cases for zero, one-bit, power-two, two-bits, byte-bits, higher-power, large-two-bits. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import population_count'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
