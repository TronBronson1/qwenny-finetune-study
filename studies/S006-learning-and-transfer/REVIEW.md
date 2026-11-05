# S006 pre-execution design review
November 4, 2026. Reviewer: coordinating agent, self-review in a separate review pass. No independent agent/human scientific review is claimed. User reviewed program documents and explicitly requested proceeding with this proposal.

## Findings and dispositions
- **Exposure:** all development targets were used in teacher-forced loss; labels explicitly retain this limit. DV001/DV002 excluded from new generation sample.
- **Selection:** fixed length-spanning rule, lowest-ID family deduplication, independent per split. This is purposive, not random/category-balanced. Exact pools and selections are retained in selection.json. No new outputs informed selection.
- **Alignment:** selected training system/user messages exactly match original corpus messages with assistant target removed. Saved prompt/token IDs are shared by all arms.
- **Scope:** original base/E1/E5 only; compact model excluded to keep this diagnostic bounded. No demonstration arm: therefore this does not settle the original adapter-versus-strong-prompt question.
- **Budget:** 24 cells, 2048 tokens each, 1200 seconds per cell, 10800 seconds total for model preflight plus generation; time checks occur at token boundaries. Scoring/reporting outside this GPU budget. Prior direct-answer examples took roughly 148 seconds for 1284 tokens; newer long-thinking runs were slower. Three-hour ceiling is a guard, not a runtime promise.
- **Completion:** eight supplied targets are 455–1554 supervised tokens, below the fixed output cap. This does not guarantee model completion.
- **Scoring infrastructure:** use established Python3.15/pytest9.2, separate from model environment. Freeze coverage before generation. Preflight all selected gold suites against reference and three designated mutants.
- **Integrity:** pinned base verification, exact E1/E5 reload probes, saved source/prompt/checkpoint hashes. No changes to historical artifacts.
- **Stop rules:** no retry on OOM/probe failure/infrastructure exception. Preserve partial output; report missing cells. A timed-out answer remains a failed first attempt. Do not close other apps or alter power plans.
- **Review limitation:** automatic gold/fixture checks and self-review improve integrity but do not establish independent semantic dataset validation.

Design disposition: ready to freeze only if scoring preflight passes, hashes are recorded, and generation implementation parses. Any preflight failure is fixed before freeze, not counted as a model result.

