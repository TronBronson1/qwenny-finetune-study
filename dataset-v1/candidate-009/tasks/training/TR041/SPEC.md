Function contract: parse_int_pair(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require two comma-separated signed canonical ASCII decimal integers. Each component is at most 12 digits excluding an optional minus; '-0' is permitted. No plus, whitespace or leading zeros except 0. Invalid syntax raises ValueError. Return a tuple of two ints.

Return type: exact built-in two-item tuple of exact built-in ints.

Coverage expectations: include normal cases for zeros, negative-zero, signed-pair, maximum-length, both-components-max-length. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import parse_int_pair'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
