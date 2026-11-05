Function contract: reverse_words(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Split on arbitrary Unicode whitespace and return words in reverse order, joined by single ASCII spaces. Empty/all-whitespace input returns the empty string.

Return type: exact built-in str.

Coverage expectations: include normal cases for empty, whitespace-only, one-word, reverse-order, mixed-whitespace, unicode-whitespace. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import reverse_words'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
