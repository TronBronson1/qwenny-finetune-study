Function contract: encode_rgb(red, green, blue).

- red: exact built-in int; reject bool and int subclasses.

- green: exact built-in int; reject bool and int subclasses.

- blue: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require every component in 0..255, otherwise ValueError. Return exactly seven characters '#rrggbb' using lowercase hexadecimal.

Return type: exact built-in str.

Coverage expectations: include normal cases for zero-components, maximum-components, ordinary, mixed-boundaries. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import encode_rgb'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
