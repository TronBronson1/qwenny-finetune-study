# Independent audit: candidate-007 rubric mutants

**Question.** Did `dataset-v1/candidate-007` fix the known gold/rubric gaps of candidate-006, and which gaps remain or are new?

**Scope.** All 60 training and 12 development tasks. Final/regression (EV/RG) tasks are absent from the checkout. They were not recreated or guessed, and the harness asserts that no EV/RG id is processed. No existing repository file was modified. Generated mutant sources go to `build/` (git-ignored); results are in `results/`.

**Rerun with one command** (repository root; needs Python ≥ 3.11 and pytest):

```bash
python3 independent-review/c007-rubric-audit/run_audit.py
```

The run takes about 10 minutes on 4 cores. It rewrites `results/audit-results.json`, `results/summary.json` and `results/TABLES.md`. This narrative was written from the run at commit `b0e0227` (Python 3.13.18, pytest 9.2.0). The numbers below are in `results/summary.json`.

## Method

1. **Reference.** Each task's `evaluator/reference/subject.py` is byte-identical in candidate-006 and candidate-007; this is checked per task.
2. **Rubric mutants.** Each mutant is the unchanged reference with one appended override that violates **one** stated requirement. The source is `mutants_lib.py`.

   | Family | What the mutant does |
   |---|---|
   | `type-subclass` | Accepts a subclass at one argument position and one stated nesting level |
   | `type-bool` | Accepts `bool` where an exact `int` is required, at one position and level |
   | `type-ordinary` | Accepts any *non-instance* (an ordinary wrong type) at one position and level, while still rejecting subclasses and bool |
   | `return-subclass`, `return-swap` | Returns a subclass, or swaps list/tuple and bool/int, at one level of the result |
   | `order` | Reports a value/shape error that is present alongside a type error, which the contract says must be reported second |
   | `exception-class` | Raises TypeError as ValueError, ValueError as TypeError or IndexError, or IndexError as ValueError |
   | `mutation-valid` | Appends to or sorts a list argument in place after a successful call, or mutates nested rows/elements |
   | `mutation-error` | Appends to a list argument, then re-raises. This is contract-only: the coverage expectations require before/after checks on *valid* calls only. |
   | `ascii` | Unicode-digit folding, NFKC normalisation, or a Unicode-aware predicate (`[0-9]`→`\d`, `"a"<=c<="z"`→`c.islower()`, …). Applied only where the SPEC states an ASCII rule. |
   | `case` | Lowercases or uppercases text inputs, or the output, where the SPEC states case behaviour |
   | `boundary` | Single-site comparison flip (`<`↔`<=`, `>`↔`>=`), integer literal ±1 on a comparison/range/len line, or regex quantifier ±1 |

3. **Concrete difference.** For each task, a seeded generator builds 900 to 13,000 probe inputs (`probes.py`). They include all gold inputs from both candidates, single-position substitutions, element insertions, mixed-invalid pairs, Unicode/fullwidth/case variants and random tuples. The probes are run on the reference and on every mutant, comparing return value with exact types at every level, the raised exception class, and the argument state after the call. Each call has a 0.25 s timeout. A mutant counts only if a witness input shows a difference. That witness is then **re-verified in a fresh subprocess** from the written mutant file: 973 of 973 were confirmed. The other 161 mutants showed no difference and are excluded as equivalent or not applicable, for example a list/tuple swap on an `int` return or an order mutant for a task with no value checks.
4. **Gold runs.** Each candidate's `test_target.py` is run with pytest against the reference and each confirmed mutant, 2,090 runs in all. Each run uses a fresh temporary directory with an empty `pytest.ini`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-p no:cacheprovider` and a 120 s timeout, and results come from JUnit XML.
   - A **gap** is a confirmed mutant whose gold suite exits 0 with at least one test.
   - Five boundary mutants loop forever and hit the timeout in both candidates. A hanging suite does not accept the implementation, so they count as killed; they are listed under Anomalies in `TABLES.md`.

## Headline results

| | candidate-006 | candidate-007 |
|---|---:|---:|
| Gold suites passing their reference | 72 / 72 | 72 / 72 (1,475 cases, matching the S007 certificate) |
| Confirmed rubric mutants surviving the gold suite (all families) | **121** | **76** |
| …excluding contract-only error-path mutation | 102 (48 tasks) | **57 (33 tasks)** |
| Training tasks with a surviving mutant (excl. error-path mutation) | 38 / 60 | 26 / 60 |
| Development tasks with a surviving mutant (excl. error-path mutation) | 10 / 12 | 7 / 12 |
| Fixed by 007 / still open / new in 007 | — | **45 / 76 / 0** |

Candidate-007 is a strict improvement: it introduced **no** new gap. It is not yet a complete rubric. Per-task and per-mutant tables with witnesses are in `results/TABLES.md`.

### Previously reported gaps

| Gap (from `program/reviews/review-002`) | 006 | 007 |
|---|---|---|
| TR038 non-ASCII hex digits | gap | **fixed** |
| TR043 non-ASCII binary digits | gap | **fixed** |
| TR056 non-ASCII RGB hex digits | gap | **fixed** |
| DV010 non-ASCII RPN digits | gap | **fixed** |
| DV008 case-insensitive comparison | gap | **fixed** |
| DV011 int-subclass endpoints | gap | **fixed** |
| TR044 non-ASCII decimal endpoints | gap | **still open** (see N1) |
| 16 list tasks without a plain wrong-type element (TR026–TR036, TR058, TR059, DV004, DV009, DV011), e.g. TR027 `pairwise_differences(['x'])` returning `[]` | 16 / 16 gaps | **16 / 16 fixed** at the element level |

For TR044, the gold now kills digit-folding and NFKC mutants with `'[١:٣]'` and `'[１:３]'`. It does not kill the realistic `[0-9]`→`\d` bug, because the leading digit stays restricted to ASCII `[1-9]` and the gold never puts a non-ASCII digit in the *second* position. Witness: `'[0:9٩]'` → the reference raises ValueError, the mutant returns `(0, 99)`.

## Gaps still open in candidate-007

### N1. Non-ASCII digit in a non-leading position, `[0-9]`→`\d` (4 training tasks: TR037, TR041, TR042, TR044)

These are the same class of gap that review-002 reported for TR038/TR043/TR056/DV010. Witnesses: `parse_unsigned('1٠')` → 10; `parse_version('0.999.99٩')`; `parse_int_pair('…,99999999999٩')`; `parse_range('[0:9٩]')`. Each accepts input the reference rejects with ValueError.

### N2. Ordinary wrong-type witnesses that a missing check also rejects (28 mutants, 23 tasks)

These are the most frequent remaining gaps. The gold's ordinary wrong types (`None`, `1`, `b'x'`, `1.5`) **raise TypeError anyway** in an implementation that has *no* type check: iterating `None`, `'(' in 1`, `range(2, 2.5)`. So the cases look like type tests but cannot tell a checked implementation from an unchecked one.

- **str arguments.** A list of strings is iterable and gets through. `DV005/DV006/DV012/TR057(['a'])` raise ValueError or AttributeError instead of TypeError. `TR014/TR016/TR017/TR020/TR022/TR024/TR060(['a'])` *return a value*.
- **int arguments with a domain check.** `-1.5` reaches the domain check first. `TR006/TR008/TR010/TR013/TR048(-1.5)` and `TR029(width=-1.5)` raise ValueError. Mixed `TR023(-1, 1)` also raises ValueError.
- **Containers.**
  - `transpose(())` returns `[]`, and `transpose([(1,)])` accepts a tuple row (TR030).
  - `interval_union(())` returns `[]`, and `interval_union([[1, 2]])` accepts a list pair (DV011).
  - TR058 and TR059 accept list/tuple containers and fail later with ValueError.
- **Element level with a mixed value error.** `rpn_evaluate(['١', 1])` (DV010).

These follow from the coverage expectation to "test each input position and each stated nested type level with an ordinary wrong type". The finite gold meets it in letter but not behaviourally. A useful ordinary witness is one that duck-typed code would *accept*: a list of str for str, a tuple for list, a list for tuple pairs, a negative float before a domain check.

### N3. Type-before-value order without a mixed-invalid witness (DV004, DV010, DV011, TR030)

The mutant reports the value or shape error before the type error.

- DV004: `xor_checksum([-4, '1'])` raises ValueError.
- DV010: `rpn_evaluate(['+', 1])` raises ValueError. The automatically chosen witness `([1, 1],)` relies on substituted values; the hand-checked `['+', 1]` is a genuine mixed case and also differs.
- DV011: `interval_union([(1,), -1])`.
- TR030: `transpose([[], None, [1, 2, 3, 4, 5]])`.

### N4. Valid-call input mutation hidden by already-sorted inputs (TR029, TR030, TR033, TR034)

An in-place `values.sort()` after computing the result survives, because every valid gold input is already sorted. One example is `chunk_list([4, 2], 2)`.

### N5. Boundaries and off-by-ones (DV007, DV010, DV011, TR050)

- DV007: `grid_neighbors(0, 1, 1, 1)` with `column < columns` → `<=` returns neighbours instead of IndexError. The `column == columns` edge is untested.
- DV010:
  - 4-digit maximum `'9999'` and 5-digit `'10000'` are untested; the quantifier `{0,3}` ±1 survives.
  - `['4', '+']` with `len(stack) < 2` → `< 1` raises IndexError instead of ValueError.
- DV011: four merge-logic index mutants, such as comparing against the previous *low* endpoint, survive. Witness `[(2, 60), (-3, -1), (10, 100)]`.
- TR050: `columns <= 0` → `< 0` with `(0, 1, 0)` raises IndexError instead of ValueError.

### N6. Character preservation and classification (TR014, TR015, TR016, TR024, TR060)

Input normalisation survives where the SPEC requires characters to be preserved or classified as ASCII:

- TR014: collapsing *any* whitespace run (`' \n\n,'`); digit folding of `'١'`.
- TR015 / TR024: digit folding and NFKC (`'onｅ'`, `'ǅ'`).
- TR016: NFKC counts fullwidth `'Ｅ'` as a vowel.
- TR060: NFKC classifies `'ǅ'` as letters.

These mutants are deliberately artificial (input normalisation), and the requirement violated is "preserve or classify literally" rather than a validation rule. Treat them as lower priority than N1 to N5.

### N7. Contract-only: input mutation on the error path (19 mutants, 17 list-input tasks)

No gold suite checks argument state after a raised exception, for example `remove_at([], 0)` appending before raising IndexError. The SPEC says "do not mutate any input", but the coverage expectations limit preservation checks to valid inputs. This is reported for completeness, not as a calibration failure.

### Families with no surviving mutant in 007

`type-subclass`, `type-bool`, `return-subclass`, `return-swap`, `exception-class` and `case` all have zero gaps in candidate-007. Candidate-006's only `type-subclass` gap was DV011, and its `case` gaps were DV008 and TR047; all three were fixed.

## Fixed by candidate-007 (45)

- **ascii (19):** digit-folding/NFKC mutants in TR038, TR043, TR044, TR056, DV010, plus NFKC in DV002, DV006, TR014, TR037, TR041, TR042, TR046, TR057.
- **type-ordinary (19):** every element-level mutant across the 16 previously reported list tasks.
- **case (4):** DV008, TR047.
- **boundary (2):** DV007 `rows <= 0`, TR041 12-digit limit.
- **type-subclass (1):** DV011.

Each fixed row names the 007 test that kills it; see `results/summary.json` → `fixed[*].killed_by_007`.

## Limitations

- The mutant families are a finite, same-author operationalisation of the stated requirements. They do not prove exhaustive correctness. A surviving mutant shows a gold blind spot; a killed mutant does not prove the requirement is fully covered.
- Witness search is deterministic but finite. Of the 161 "no difference found" mutants, most are structurally equivalent (int/str returns, tasks without value checks). A few could hide differences outside the probe space.
- `order` mutants repair type-invalid items with neighbouring valid values. One automatically chosen witness (DV010) relied on that substitution; a genuine mixed witness was checked by hand. Witnesses for N2/N3 are in `TABLES.md` for human review.
- The runtime differs from the project's established Python 3.15 / pytest 9.2 on Windows. This run used Python 3.13.18 / pytest 9.2.0 on Linux. Reference results agree (72/72, 1,475 cases).
- No model outputs were generated, scored or rescored. Nothing here changes the frozen candidates or approvals.

## Files

| Path | Content |
|---|---|
| `run_audit.py` | Pipeline (build → witness → verify → gold → report) |
| `mutants_lib.py` | Mutant families and override templates |
| `probes.py` | Seeded probe generator and outcome comparison |
| `make_report.py` | Summaries and tables from the results JSON |
| `results/audit-results.json` | Every mutant: requirement, override, witness, fresh-process confirmation, per-candidate pytest result |
| `results/summary.json` | Totals, per-family, per-task, known-gap status, fixed/open/new lists |
| `results/TABLES.md` | Generated tables |
