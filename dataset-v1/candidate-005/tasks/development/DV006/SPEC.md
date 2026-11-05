Function contract: keypad_encode(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Accept only uppercase ASCII A-Z; other characters raise ValueError. Map to telephone keypad digits ABC=2, DEF=3, GHI=4, JKL=5, MNO=6, PQRS=7, TUV=8, WXYZ=9. Empty input returns ''.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import keypad_encode'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
