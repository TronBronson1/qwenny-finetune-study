Function contract: balanced_brackets(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Only (), [], {} characters are permitted; other characters raise ValueError. Return exact bool for correctly nested and matched brackets. Empty input is balanced; mismatches/unclosed brackets return False.

Return type: exact built-in bool.

Coverage expectations: include normal cases for empty, single-pair, nested-all-kinds, mismatched, unclosed, premature-close, reversed, concatenated. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import balanced_brackets'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
