Function contract: bounded_slice(values, start, stop).

- values: exact list of exact ints; reject bool, int subclasses and list subclasses.

- start: exact built-in int; reject bool and int subclasses.

- stop: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require 0 <= start <= len(values) and 0 <= stop <= len(values), otherwise IndexError. Return the half-open slice; start > stop returns [].

Return type: exact built-in list of exact built-in ints.

Do not mutate any input or nested mutable elements.

Coverage expectations: include normal cases for empty, full, middle, reversed-valid, end-empty, unsorted-values. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels. Compare valid inputs before and after calls.

Write one complete pytest file importing 'from subject import bounded_slice'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
