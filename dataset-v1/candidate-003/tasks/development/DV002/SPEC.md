Function contract: minute_of_day(text).

- text: an exact built-in str (reject subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Accept exactly five ASCII characters HH:MM, hours 00..23 and minutes 00..59. Return hour*60+minute as an exact int. No trimming, signs, Unicode digits or extra characters. All malformed strings raise ValueError.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import minute_of_day'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
