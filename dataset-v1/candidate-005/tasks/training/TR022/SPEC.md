Function contract: quote_csv_field(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

For a single CSV field, double each double quote and wrap the field in double quotes if it contains comma, CR, LF, or double quote. Also quote the empty field. Otherwise return it unchanged.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import quote_csv_field'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
