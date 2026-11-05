Function contract: weekday_offset(day, delta).

- day: exact built-in int; reject bool and int subclasses.

- delta: exact built-in int; reject bool and int subclasses.

Reject invalid specified types with TypeError before shape/value checks.

Require 0 <= day <= 6, otherwise ValueError. Return the weekday after adding signed delta with wraparound; weekdays are numbered 0 through 6.

Return type: exact built-in int.

Coverage expectations: include normal cases for identity, forward, wrap, negative-wrap, multiple-weeks, negative-weeks, forward-wrap. Test each input position and each stated nested type level with an ordinary wrong type and a subclass; reject bool wherever exact int is required, holding other inputs valid. Exercise stated invalid domain/shape/bounds rules and mixed-invalid witnesses for the stated validation order. Check exact returned types at the stated levels.

Write one complete pytest file importing 'from subject import weekday_offset'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use complete explicit argument tuples. Return one Python code block, then a brief requirement-to-input mapping and finite-coverage limitations. Do not claim execution.
