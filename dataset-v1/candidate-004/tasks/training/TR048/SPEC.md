Function contract: spreadsheet_column(number).

- number: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 1 <= number <= 18278, otherwise ValueError. Return the spreadsheet column label: 1=A, 26=Z, 27=AA, 702=ZZ, 703=AAA, 18278=ZZZ.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import spreadsheet_column'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
