Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution.

Function contract: remove_at(values, index).

- values: exact list of exact ints; reject bool, int subclasses and list subclasses.

- index: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require 0 <= index < len(values), otherwise IndexError (negative indices are forbidden). Return a new list with exactly that item removed.

Return type: exact built-in list of exact built-in ints.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for only-item, first, middle, last, duplicates, unsorted-values. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare valid inputs before and after calls.

Write one complete pytest file importing 'from subject import remove_at'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
