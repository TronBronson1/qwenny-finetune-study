Function contract: keypad_encode(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Accept only uppercase ASCII A-Z; other characters raise ValueError. Map to telephone keypad digits ABC=2, DEF=3, GHI=4, JKL=5, MNO=6, PQRS=7, TUV=8, WXYZ=9. Empty input returns ''.

Return type: exact built-in str.

Coverage expectations: include normal cases for empty, first-group, ordinary, pqrs, wxyz, full-alphabet. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import keypad_encode'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
