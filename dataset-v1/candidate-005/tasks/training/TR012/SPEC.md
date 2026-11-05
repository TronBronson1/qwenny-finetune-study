Function contract: weekday_offset(day, delta).

- day: an exact built-in int (reject bool and subclasses).

- delta: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require 0 <= day <= 6, otherwise ValueError. Return the weekday after adding signed delta with wraparound; weekdays are numbered 0 through 6.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import weekday_offset'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
