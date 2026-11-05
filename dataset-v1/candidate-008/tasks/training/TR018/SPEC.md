Function contract: is_palindrome(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Return an exact bool for literal, case-sensitive character palindrome equality. Do not remove punctuation or whitespace; empty input is a palindrome.

Return type: exact built-in bool.

Coverage expectations: include normal cases for empty, one, two-equal, odd-palindrome, even-palindrome, not-palindrome, case-sensitive, literal-space, unicode, literal-punctuation-and-space. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import is_palindrome'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
