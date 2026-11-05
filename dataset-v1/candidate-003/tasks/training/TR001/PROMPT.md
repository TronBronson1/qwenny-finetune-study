Function contract: batches(items, capacity).

- items: an exact built-in int (reject bool and subclasses).

- capacity: an exact built-in int (reject bool and subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

items >= 0 and capacity > 0. Return the minimum number of capacity-sized batches needed; zero items needs zero. Invalid values raise ValueError.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import batches'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
