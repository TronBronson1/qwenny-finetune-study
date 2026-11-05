Function contract: count_ascii_categories(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return a tuple (letters,digits,other) counting ASCII A-Z/a-z, ASCII 0-9, and all remaining characters respectively. Unicode letters/digits belong to other.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import count_ascii_categories'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
