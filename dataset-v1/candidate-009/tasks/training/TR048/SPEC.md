Function contract: spreadsheet_column(number).

- number: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require 1 <= number <= 18278, otherwise ValueError. Return the spreadsheet column label: 1=A, 26=Z, 27=AA, 702=ZZ, 703=AAA, 18278=ZZZ.

Return type: exact built-in str.

Coverage expectations: include normal cases for lower-bound, last-single, first-double, double-boundary, last-double, first-triple, upper-bound. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import spreadsheet_column'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
