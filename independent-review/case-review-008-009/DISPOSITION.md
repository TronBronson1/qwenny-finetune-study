# Disposition of the read-through review (`REVIEW.md`)

The review was done by a fresh-context reviewer agent working in the same session. It was read-only and judged each case against the written contract, not against mutants. That makes it more independent than the author re-reading their own work, but it is **not** an external human review.

| # | Finding | Severity | Disposition |
|---|---|---|---|
| 1 | TR030 e013 `[[1], None, [1, 2]]` does not separate type-before-shape from shape-first code; a shape-first implementation passes all 22 TR030 tests. | broken witness | **Fixed in candidate-009, amendment 1.** Added `[[1], [1, 2], None]` and `[[1], [1, 2], [True]]`, both expecting TypeError, plus designated mutant R10, which checks shape first and raises ValueError there. Candidate-008 is approved and frozen, so the weak witness remains in 008 as a documented limitation. |
| 2 | DV011 label "unordered-overlap-chain" is not a chain. | cosmetic | **Renamed in 009** to `unordered-overlap-with-disjoint`. |
| 3 | TR024/TR060 label "compatibility-characters": `١` has no compatibility decomposition. | cosmetic | **Renamed in 009** to `compatibility-and-nonascii-digit`. |
| 4 | "unsorted-values/rows" labels for order-insensitive functions could suggest order matters. | cosmetic, low | **Left unchanged.** The labels describe the inputs accurately, and the case exists to catch in-place sorting. Revisit if model outputs show confusion. |
| 5 | DV001: "compare inputs before and after every call" read literally invites deepcopy-then-`==` on `object()`, which fails even without mutation. | ambiguity | **Fixed in 009.** DV001's sentence adds: "Compare arbitrary element objects by identity, not by copied value." |
| 6 | DV001's raise-path snapshot can never fail, because no invalid DV001 input holds mutable content. | cosmetic | **Left unchanged.** It is harmless and keeps the instruction uniform. |
| — | Candidate-009 soundness: `deepcopy(a) == a` holds for all 422 invalid inputs; `==` ignores element type. | limitation | Documented. A type-swapping mutation of equal value would go unnoticed; no audit mutant does this. |

None of the 60 candidate-008 cases contradicts its contract.
