# Next training study brief — value-focused targets

Status: design brief, not frozen or executed. Prepared after S007/S008, November 4, 2026.

## Question

Do short, independently verified calculation comments beside normal-return cases improve first-attempt correctness compared with the same calibrated targets without those comments?

S008 shows that some errors remain even when inputs are supplied and no pytest file is required. This motivates a value-focused intervention; it does not establish that comments will work. Repeated extra epochs or a precision change would test different hypotheses.

## Proposed controlled comparison

- Unchanged pinned base as inference control.
- Fresh adapter trained on candidate-007 with the explicit fit overlay.
- Fresh adapter trained on the same examples, cases, executable AST and fit presentation, adding short verifiable calculation comments to selected training return-value rows only.

Choose the training comment families and expressions from contracts/oracles before any new model answers. Never use failed development outputs as targets. Keep development targets outside optimizer training. Comments must be checked as factual expressions; no fabricated hidden-reasoning traces are needed.

Hold base revision, tokenizer, NF4/BF16 runtime, rank/scope, optimizer, seed42, task order, five passes and 75 updates fixed. E5 is the predeclared endpoint for each trajectory; other saved checkpoints are not a post-hoc winner pool. Fixed updates are not equal FLOPs or supervised-token exposure when comments add tokens: record these differences and limit claims accordingly.

If comments exceed 2048 complete-chat tokens, apply the same AST-preserving presentation change to both arms before freeze, or revise the treatment prospectively. No truncation or silent longer-sequence budget.

## Required implementation gates

1. Explicit export/provenance and current authorization record for the actual changed corpus/overlay; do not inherit the old hash approval silently.
2. All revised targets/comments pass the gold/rubric/mutant gate, and every added expression agrees with the separate oracle and reference.
3. Exact assistant-only token masks and decoded supervised spans; no role, prompt or development labels trained.
4. Actual longest-example forward/backward, finite intended gradients, no base updates, save/reload probes and local memory checks.
5. A model-suite scorer with contract-specific witness binding and a frozen wrong-exception policy. S007's gold-only structural predicate is not a general model-suite semantic scorer.
6. Freeze task IDs, measures, inference settings, compute ceiling and decision rule before execution. No final/regression inspection for this selection.

## Evaluation proposal to resolve before freeze

Use the visible eight-task development/training diagnostic pool, reporting familiar and development results separately. Primary full-suite measure: reference-valid first attempts. Secondary: completion/collection, task-macro requirement evidence, strict v2 acceptance and supported/unsupported prose claims. Reference-invalid suites receive no eligible mutant-credit denominator; report them separately. Use S008-style supplied-value scoring only as a separate component measure.

Within this new comparison, use identical cleaned prompts and direct-answer generation settings across all three arms. A concrete starting proposal is seed42, temperature1/top_k20/top_p.95, presence0/repetition1, cap2048/context16134. This is not directly comparable to greedy value-only S008. No repairs, retries or best-of-N.

Plan a local-only bounded GPU allocation using the observed training and generation timings; worst-case output costs, not just optimizer minutes, must fit the declared ceiling. Preserve aborted arms rather than fabricate a paired conclusion. No cloud, app closure, working-model replacement, merge or export to LM Studio under this brief.

## Decision boundary

If the treatment improves reference-valid task behavior without losing required coverage, confirm under a frozen broader development protocol before selecting a candidate. If not, report the negative/ambiguous finding and revisit the hypothesis. No result here is sufficient by itself for deployment or a general coding-improvement claim. The original practical question still requires a strong prompted-base comparison, regression checks and appropriately frozen held-out evaluation.
