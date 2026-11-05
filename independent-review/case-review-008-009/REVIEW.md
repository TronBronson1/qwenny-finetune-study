# Independent review: candidate-008 cases and candidate-009 raise-path snapshots

**Summary:** I reviewed 60 declared candidate-008 cases: 17 valid and 43 invalid. 59 match the contract with no issue. 1 has a defective witness. None of the 60 contradicts its contract. On top of that there are 3 cosmetic label notes. Candidate-009 covers 19 tasks: the snapshot assertion is sound on all of them, and there is 1 low ambiguity in wording for DV001. Total concerns: 6 (0 error, 1 witness defect, 1 ambiguity, 4 cosmetic).

How I checked:
- Every declared case is present in candidate-008 `evaluator/cases.json` with the same args, expected value or exception, and label.
- I recomputed every expected value by hand from SPEC.md.
- All candidate-008 and candidate-009 gold suites (TR/DV only) pass against `evaluator/reference/subject.py`.
- candidate-008 differs from candidate-007 only in the 11 coverage lists of the valid-case tasks.
- candidate-009 differs from candidate-008 only in the one sentence, in all 19 tasks. TARGET.md prose was updated to match.

## Concerns

| # | Task | Case args | Label | Gold expects | Contract says | Severity | Suggested fix |
|---|---|---|---|---|---|---|---|
| 1 | TR030 (c008 e013) | `([[1], None, [1, 2]],)` | type-before-shape | TypeError | "Reject invalid specified types with TypeError before shape/value checks." TypeError is correct. | cosmetic, but substantive: the witness does not discriminate | The input is not a real ordering witness. `None` sits before the ragged row, and a shape-first check calls `len(None)`, which raises TypeError anyway. I confirmed this with a shape-first mutant: it checks rectangularity before row and element types and **passes all 22 TR030 gold tests**. No TR030 case separates the two orders at row level. Replace it with `([[1], [1, 2], None],)` or `([[1], [1, 2], [True]],)`. The mutant raises ValueError on both, while the contract requires TypeError. |
| 2 | DV011 (c008 v008) | `([(2, 60), (-3, -1), (10, 100)],)` | unordered-overlap-chain | `[(-3, -1), (2, 100)]` (correct) | n/a | cosmetic | This is not a chain. Only two intervals overlap, plus one disjoint interval. "chain" also blurs it with the existing `transitive-unordered-union`. Rename to e.g. `unordered-overlap-with-disjoint`. |
| 3 | TR024 v005, TR060 v005 | `('ǅ١ｅ',)`, `('ǅＡ١',)` | compatibility-characters | `'ǅ١ｅ'`, `(0, 0, 3)` (both correct) | n/a | cosmetic (low) | U+0661 `١` has no compatibility decomposition. The label fits only ǅ and the fullwidth characters. Possible labels: `nonascii-titlecase-fullwidth-digit` or `compatibility-and-nonascii-digit`. |
| 4 | TR029 v006, TR033 v005, TR034 v005, TR030 v006 | `([4,2],2)`, `([4,2],0)`, `([3,1,2],0,3)`, `([[2,1],[0,3]],)` | unsorted-values / unsorted-rows | `[[4,2]]`, `[2]`, `[3,1,2]`, `[[2,0],[1,3]]` (all correct) | n/a | cosmetic (low) | These functions have no ordering semantics. In the model-visible list the label could suggest that order matters, while the real purpose is to expose in-place sorting. Acceptable as is; `non-monotonic-values` would be more neutral. |
| 5 | DV001 (c009 wording) | n/a | n/a | Raise-path snapshots, plus `test_identity_and_no_element_mutation`, which takes no deepcopy snapshot | "values: exact tuple of arbitrary objects" plus "Compare inputs before and after every call, including calls that raise." | ambiguity (low) | Read literally, "every call" asks for `deepcopy` then `==` on inputs that hold `object()`. That comparison is False with no mutation at all, so a model obeying it would write a suite that fails against the correct implementation. The gold rightly does not do this. Add to DV001: "(compare arbitrary objects by identity / per-element state)". |
| 6 | DV001 (c009 suite) | all 8 `test_raises_typeerror` inputs | n/a | `args == before` | n/a | cosmetic (low) | The new assertion can never fail here. No invalid input holds mutable content; the only list is `[]`. Sound, but it checks nothing. Optional fix: add an invalid case with mutable content, e.g. `(([1],), IntChild(0))` → TypeError. |

Note on candidate-009, not counted as a concern: `==` ignores type, so `True == 1`, `IntChild(1) == 1` and `ListChild([1]) == [1]` all hold. The snapshot therefore misses in-place mutations that swap an element for an equal value of another type. This weakens the check but does not make it unsound. The candidate-008 valid-path checks have the same property.

## Candidate-009 soundness check (19 tasks)

Tasks: DV001, DV004, DV009, DV010, DV011, TR025–TR036, TR058, TR059.

- Each `test_raises_*` now has `before=copy.deepcopy(args)` … `assert args == before`. There are 29 raise functions in total, all covered.
- I loaded all 422 invalid inputs. Their types are limited to int, bool, float, str, None, list and tuple, plus the plain subclasses IntChild, ListChild, StrChild and TupleChild, none of which overrides `__eq__`.
- None of the inputs contains NaN, an identity-only object, a generator or a custom `__eq__`.
- For every input, `deepcopy(a) == a` holds.
- The reference raises without mutating, and all suites pass.
- The wording "Compare inputs before and after every call, including calls that raise." is clear everywhere except the DV001 note above (#5).
- The other 52 TR/DV tasks have no mutable specified inputs and no comparison sentence, which is consistent.

## Cases checked and found fine

**Valid (c008):**
- TR029 `([4,2],2)`→`[[4,2]]`
- TR030 `[[2,1],[0,3]]`→`[[2,0],[1,3]]`
- TR033 `([4,2],0)`→`[2]`
- TR034 `([3,1,2],0,3)`→`[3,1,2]`
- DV010 `['9999']`→9999, `['-9999']`→-9999
- DV011 `[(1,4),(2,6)]`→`[(1,6)]`; v008 value correct; `[(1,2),(26,27),(25,130),(25,256)]`→`[(1,2),(25,256)]`
- TR014 `'a\n\nb'`, `'a\t\tb'`, `'a \t\nb'` returned unchanged; `'٣  ４'`→`'٣ ４'`
- TR015 `'١  ｅ'`→`'ｅ ١'`
- TR016 `'Ｅá'`→0
- TR024 and TR060 values correct

**Invalid (c008):** the exception class follows the contract and the label holds in each case.

- **ascii-nonleading-digit → ValueError:**
  - TR037 `'1٠'`
  - TR041 `'1٠,2'`, `'1,2٠'`
  - TR042 `'1٠.0.0'`, `'0.0.1٠'`
  - TR044 `'[0:1٠]'`, `'[1٠:20]'`
  - Each is a genuine `\d` witness: `int()` accepts these strings.
- **ordinary-iterable → TypeError:**
  - DV005 `['(']`, DV006 `['A']`, DV012 `['(']`
  - TR014, TR016, TR020, TR022, TR024, TR057, TR060 `['a']`
  - TR017 `(['a'],'b')`, `('a',['b'])`
  - Duck-typed code would accept or misreport each of these.
- **ordinary-before-domain → TypeError:**
  - TR006, TR008, TR010, TR048 `-1.5`
  - TR013 `(-1.5,2)`
  - TR023 `(-1,1)`
  - TR029 `([1],-1.5)`
  - Each discriminates a domain-first check.
- **TR030:** `((),)` and `([(1,)],)` → TypeError. These are correct ordinary container and row witnesses. e013 is covered under #1.
- **TR058:** `([0,0,0],(0,0,0,0))` and `((0,0),[0,0,0])` → TypeError. Both discriminate a shape-first check.
- **TR059:** `((2,1),[])` and `([], (2,1))` → TypeError. Both discriminate an order-first check.
- **DV004:** `[-1,'x']` → TypeError. Discriminates per-item interleaved checks.
- **DV010:**
  - `['+',1]` → TypeError, which discriminates evaluate-as-you-go.
  - `['10000']` → ValueError (5 digits).
  - `['4','+']` → ValueError (insufficient operands).
- **DV011:**
  - `((),)` and `([[1,2]],)` → TypeError.
  - `([(1,),-1],)` → TypeError. This is a genuine witness: a per-pair shape check raises ValueError on `(1,)` first, and the gold treats wrong pair length as ValueError (e014).
- **DV007:** `(0,1,1,1)` and `(1,0,1,1)` → IndexError. These are the off-by-one bounds cases.
- **TR050:** `(0,1,0)` → ValueError. Correct and also an order witness: the contract checks dimensions before the index ("Then"), so an index-first check would raise IndexError.
