Function contract: quote_csv_field(text).

- text: exact built-in str; reject str subclasses.

Reject invalid specified types with TypeError before shape/value checks.

For a single CSV field, double each double quote and wrap the field in double quotes if it contains comma, CR, LF, or double quote. Also quote the empty field. Otherwise return it unchanged.

Return type: exact built-in str.

Coverage expectations: include normal cases for empty-quoted, unquoted, comma, quote-doubled, cr, lf, preserve-space, unicode. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import quote_csv_field'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
