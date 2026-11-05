Function contract: parenthesis_depth(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Only '(' and ')' are permitted. Require a balanced sequence with no premature closing parenthesis, otherwise ValueError. Return maximum nesting depth as int; empty input returns 0.

Return type: exact built-in int.

Coverage expectations: include normal cases for empty, one-pair, nested, siblings, deep. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import parenthesis_depth'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
