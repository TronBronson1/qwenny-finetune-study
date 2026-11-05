Function contract: parse_unsigned(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require a canonical unsigned decimal literal of 1 through 12 ASCII digits: either '0' or a nonzero digit followed by digits. No signs, whitespace or leading zeros. Invalid syntax/length raises ValueError. Return int.

Return type: exact built-in int.

Coverage expectations: include normal cases for zero, one, ordinary, maximum-length. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import parse_unsigned'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
