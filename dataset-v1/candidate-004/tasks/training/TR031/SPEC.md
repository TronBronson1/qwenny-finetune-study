Function contract: multiset_intersection(left, right).

- left: an exact list of exact ints (reject bool, subclasses and list subclasses).

- right: an exact list of exact ints (reject bool, subclasses and list subclasses).

Reject invalid specified types with TypeError before value/shape checks. All returned containers/scalars must have exact built-in types as described, recursively.

Return the multiset intersection, in left-input order: each value occurs at most its count in right. Do not mutate either input.

Do not mutate any input, including nested containers.

Write one complete pytest file importing 'from subject import multiset_intersection'. Do not implement, replace, mock or inspect the function. Use only pytest and the standard library. Use explicit complete argument tuples. Return one Python code block, then a brief requirement-to-input mapping and honest finite-coverage limitations. Do not claim execution.
