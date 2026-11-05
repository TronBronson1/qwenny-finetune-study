Function contract: plural_count(number, noun).

- number: exact built-in int; reject bool and int subclasses.

- noun: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require number >= 0 and nonempty noun, otherwise ValueError. Return '<number> <noun>' for 1, and append exactly 's' to noun otherwise. This is literal formatting, not English inflection.

Return type: exact built-in str.

Coverage expectations: include normal cases for zero-plural, one-singular, ordinary-plural, literal-singular, literal-suffix, unicode-noun. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import plural_count'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
