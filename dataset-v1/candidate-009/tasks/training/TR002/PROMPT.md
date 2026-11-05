Write executable pytest tests for the supplied contract. Use complete explicit argument tuples. Keep normal-return cases separate from expected-exception cases. Check expected results against concrete arguments. Follow the explicit coverage expectations; do not invent identity, nesting or bounds requirements. Distinguish inspection from execution and do not claim execution.

Function contract: strip_prefix(text, prefix).

- text: exact built-in str; reject str subclasses.

- prefix: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

prefix must be nonempty, otherwise ValueError. Remove exactly one case-sensitive literal prefix if present at the start. Preserve whitespace and Unicode; empty text is valid.

Return type: exact built-in str.

Coverage expectations: include normal cases for remove-prefix, whole-prefix, absent-prefix, empty-text, remove-once, case-sensitive, start-only, space-prefix, unicode-prefix, long-prefix. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import strip_prefix'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
