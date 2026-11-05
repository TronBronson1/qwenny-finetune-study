Function contract: seconds_to_hms(seconds).

- seconds: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Require seconds >= 0, otherwise ValueError. Return (hours,minutes,seconds), without wrapping hours at 24; minutes/seconds are each 0..59.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import seconds_to_hms'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
