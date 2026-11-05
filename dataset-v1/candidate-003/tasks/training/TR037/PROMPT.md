Function contract: parse_unsigned(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require a canonical unsigned decimal literal of 1 through 12 ASCII digits: either '0' or a nonzero digit followed by digits. No signs, whitespace or leading zeros. Invalid syntax/length raises ValueError. Return int.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import parse_unsigned'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
