Function contract: collapse_spaces(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Replace each nonempty run of ASCII space U+0020 with one space. Preserve leading/trailing single spaces, tabs, newlines and all other characters.

Return type: exact built-in str.

Coverage expectations: include normal cases for empty, unchanged, spaces-only, edges-and-run, preserve-tab, preserve-lf, unicode, preserve-nbsp. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import collapse_spaces'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
