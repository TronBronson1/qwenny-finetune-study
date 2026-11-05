Function contract: rpn_evaluate(tokens).

- tokens: an exact list of exact strings (reject subclasses at both levels).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 1..32 tokens forming one reverse-Polish expression. Integers use optional minus and canonical 1..4 ASCII digits (zero and '-0' allowed). Operators are '+', '-', '*'. Insufficient operands, extra operands, invalid tokens/length raise ValueError. Return exact int; do not mutate tokens.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import rpn_evaluate'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
