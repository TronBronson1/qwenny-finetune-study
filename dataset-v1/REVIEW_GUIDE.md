# Independent review guide

The assembly task is complete; this guide is the quality gate before training.
Your earlier review of feasibility results did not approve these newly authored
examples. Project 03_DATASET_RULES.md calls for reviewed successful targets and a
family-level split, so independent review is recorded separately from automated checks.

For each training row, read SPEC.md and TARGET.md together. Trace every explicit
argument tuple, result and exception. Check exact built-in types (including bool
and subclass rejection), value/type precedence, empty/boundary cases, and any
mutation/identity rule. Verify that the target imports only the stated function
and does not implement or inspect it. Check the brief mapping and limitations.

Then examine the separate oracle method and each mutant's concrete witness.
Check that the reference agrees with the written contract, that rejection cases
are intentional, and that mutants are genuine single defects rather than equivalent
implementations. Passing one reference alone is not sufficient. Bounded oracle
checks and generated cases are not an independent person's review.

Audit function/problem-family similarity across all four splits. The automated
check removes names/literal values and looks for exact structural clones; it cannot
certify semantic novelty. A renamed or constant-changed variant must remain with
its family. Existing rotation/clock development tasks and earlier visible tasks
cannot be presented as unseen final tests.

Record a real reviewer identity, exact hashes, decision and concrete notes in a
copy of approvals.template.json. Do not overwrite the candidate snapshot or forge
a reviewer/approval. Fixes require a new candidate and validation of changed content.
The export guard requires all 60 training records and the family audit to be approved.
Final/development/regression target reviews remain necessary before formal scoring.

Before training, pin the reasoning/direct-answer policy, verify assistant-only
masking and nonzero target tokens, fit full examples without truncation, and repeat
matched base A/B controls in the eventual runtime. Only then compare an adapter.
