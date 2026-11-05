Function contract: edit_distance(left, right).

- left: exact built-in str; reject str subclasses.

- right: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return Levenshtein distance with insertion, deletion and substitution cost 1; equal characters cost 0. Compare literal Unicode characters case-sensitively.

Return type: exact built-in int.

Coverage expectations: include normal cases for both-empty, left-empty, right-empty, equal, substitution, two-edits, multistep, unicode-accent, ascii-case-sensitive, unicode-case-sensitive, literal-codepoints-no-normalization. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import edit_distance'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
