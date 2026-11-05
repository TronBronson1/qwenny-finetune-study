Function contract: parse_bool_word(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Accept exactly 'true' and 'false' in lowercase. Return exact bool. Any other string raises ValueError.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_bool_word'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
