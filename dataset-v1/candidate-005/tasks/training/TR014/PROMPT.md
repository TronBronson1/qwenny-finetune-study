Function contract: collapse_spaces(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Replace each nonempty run of ASCII space U+0020 with one space. Preserve leading/trailing single spaces, tabs, newlines and all other characters.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import collapse_spaces'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
