Function contract: index_of_nth(text, needle, occurrence).

- text: exact built-in str; reject str subclasses.

- needle: exact built-in str; reject str subclasses.

- occurrence: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require nonempty needle and occurrence >= 1, otherwise ValueError. Matches are literal and case-sensitive. Return the start index of that occurrence, counting overlapping matches; return -1 if absent.

Return type: exact built-in int.

Coverage expectations: include normal cases for empty, first-overlap, second-overlap, third-overlap, missing-overlap, whole-string, absent, unicode, literal-case, no-second-case-match. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import index_of_nth'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
