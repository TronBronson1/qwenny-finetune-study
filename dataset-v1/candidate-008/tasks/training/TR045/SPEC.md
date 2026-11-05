Function contract: path_segments(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Split on literal '/' and discard empty segments only. Preserve '.', '..', backslashes, spaces and all other characters; this is not path normalization.

Return type: exact built-in list of exact built-in strings.

Coverage expectations: include normal cases for empty, separator-only, repeated-separators, literal-dot-segments, literal-backslash, space-unicode. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import path_segments'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
