Function contract: seconds_to_hms(seconds).

- seconds: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require seconds >= 0, otherwise ValueError. Return (hours,minutes,seconds), without wrapping hours at 24; minutes/seconds are each 0..59.

Return type: exact built-in three-item tuple of exact built-in ints.

Coverage expectations: include normal cases for zero, last-second, minute, last-minute, hour, hours-over-day. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import seconds_to_hms'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
