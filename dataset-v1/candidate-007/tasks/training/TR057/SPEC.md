Function contract: make_slug(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Only ASCII letters, digits, space, hyphen and underscore are permitted; other characters raise ValueError. Treat space/hyphen/underscore runs as separators, lowercase letters and join nonempty parts by one hyphen. All-separator input returns ''.

Return type: exact built-in str.

Coverage expectations: include normal cases for empty, separators-only, lowercase, separator-runs, digits. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import make_slug'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
