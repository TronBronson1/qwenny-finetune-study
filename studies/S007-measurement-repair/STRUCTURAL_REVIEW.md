# Structural advisory dispositions

All 72 revised targets were scanned with the archived external checker. No ordinary-type, subclass or ASCII-digit absence flags remain. The remaining eight automatic keyword flags are false positives for the reasons below; three validation-order notices require semantic inspection rather than a keyword decision.

| Task | Advisory | Disposition / concrete evidence |
|---|---|---|
| TR002 | No whole input strings differing only by case | Prefix behavior is distinguished by ('Abc','a'): literal comparison retains 'Abc', case-folded comparison would return 'bc'. |
| TR018 | No pair of case-differing strings | This function takes one string: 'Aa' is not a literal palindrome, but is one after lowercasing. |
| TR047 | No whole strings differing only by case | Added ('Aa','a',1) returns 1 rather than case-folded index 0. Input text need not have the same length as its needle to test case sensitivity. |
| TR023 | No valid empty case | An empty noun is forbidden and is tested as ValueError, not as a valid empty return case. |
| TR036 | No valid empty case | Empty values are forbidden and tested as ValueError. |
| TR040 | No valid empty text | Empty text is forbidden; an empty value in 'a=' is valid and covered. |
| TR042 | No valid Unicode input | Unicode digits are forbidden and tested as invalid; the checker only looked at valid cases. |
| DV002 | No valid Unicode input | Unicode digits are forbidden and tested as invalid, including Arabic-Indic and fullwidth examples. |
| TR049/TR050/DV007 | Inspect shape-before-bounds | Zero dimensions with zero/nonnegative coordinates are simultaneously invalid shapes and out-of-bounds cells. Gold requires ValueError before IndexError. Type-before-value mixed cases are also retained. DV007 now includes zero/negative columns. |

This is same-agent finite semantic review using contracts, literal case tables, oracle/reference checks and executable witnesses. The archived raw structural output remains available. It is not an independent review of all 72 tasks or proof that every possible contract defect is covered.

The task-specific normal-return category maps are in candidate-007 task rubric.json files and the builder's repair_config.py. They were reviewed against all 72 parent contracts and valid-case tables. Additional finite cases address literal punctuation, left-input order, stable partition order, numeric component bounds, case-sensitive indexing, negative currency, long RPN expressions and transitive interval union. All new expected values were checked against the original separate valid-domain oracle and unchanged reference. No failed model output became a training answer.

Some target presentation remains deliberately repetitive; loss/case rebalancing and calculation-comment training are deferred rather than conflated with this measurement repair.

