Function contract: leap_year(year).

- year: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require 1 <= year <= 9999, otherwise ValueError. Return an exact bool under the proleptic Gregorian leap-year rule.

Return type: exact built-in bool.

Coverage expectations: include normal cases for lower-bound, divisible-four, century-not-leap, century-leap, ordinary-not-leap, ordinary-leap, future-century, upper-bound. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import leap_year'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
