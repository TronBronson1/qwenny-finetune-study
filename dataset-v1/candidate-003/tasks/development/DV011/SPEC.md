Function contract: interval_union(intervals).

- intervals: an exact list of exact two-int tuples.

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Each pair is (low,high) with low < high, otherwise ValueError. Return sorted nonoverlapping half-open interval pairs covering the union; merge overlaps and touching intervals. Input order is arbitrary. Do not mutate input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import interval_union'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
