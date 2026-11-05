Function contract: parse_key_value(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Split on the first literal '='. The key must be nonempty; the value may be empty or contain '='. Preserve all characters. Missing '=' or empty key raises ValueError. Return a (key,value) tuple.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_key_value'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
