Function contract: balanced_brackets(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Only (), [], {} characters are permitted; other characters raise ValueError. Return exact bool for correctly nested and matched brackets. Empty input is balanced; mismatches/unclosed brackets return False.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import balanced_brackets'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
