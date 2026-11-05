# Roles and workflow
## Responsibility
The user is sponsor and observer: defines purpose, priorities, resource boundaries, and receives understandable reports. The team handles routine technical preparation within authorization.

| Role | Owns | Must hand off |
|---|---|---|
| Orchestrator | Current state, work queue, scope, execution ownership and resource checks | One explicit assignment and acceptance criteria at a time |
| Study designer | Question, competing explanations, comparisons, measurements, sample selection and stop rules | Reviewable protocol before execution |
| Developer | Implementation, manifests, reproducible commands and infrastructure checks | Code and evidence of preflight; no unilateral scientific scope changes |
| Tester / reviewer | Evaluator validity, protocol compliance, data boundaries, source review and result audit | Findings with severity, evidence, and disposition |
| Synthesizer | Evidence-to-claim mapping and accessible explanation | Technical conclusion plus observer report and glossary updates |

These are functional roles, not a claim that separate agents have already reviewed the work. One agent can prepare multiple artifacts, but must label self-review honestly. Where separate-agent review is used, give the reviewer the protocol and original evidence rather than only the author's conclusion. Agreement among agents is not independent scientific replication.

## Gates
1. Intake: state the question and why the result would change a decision.
2. Design: specify arms, task IDs, prompts, generation settings, scoring, resource budget and stop rules.
3. Review: resolve material design/evaluator issues. Record reviewer identity and limitations.
4. Freeze: save protocol and implementation hashes, exact inputs, and execution environment.
5. Preflight: validate imports, stop tokens, output storage, evaluator interpreter and isolation. Distinguish a smoke check from a scored answer.
6. Execute: one GPU owner; preserve first attempts and partial outputs. Log infrastructure failures separately.
7. Test: inspect/hash-bind candidate source and use unchanged isolated fixtures. No mutant credit for reference-invalid suites.
8. Synthesize: report all cells and uncertainty; update study register, decisions, current state, and observer report.
9. Decide: continue, change one justified factor, stop, or prepare final evaluation.

### Mandatory gold/rubric calibration gate

Before a new dataset/evaluation freeze, assess every gold answer against the same applicable model-facing instructions and rubric used for model answers. Record each requirement's gold witness, relevant mutant witness or documented review method, and any ambiguity. Structural flags are review leads, not automatic failures. Gold must pass the correct reference and reject every designated valid mutant through meaningful checks; mere nonzero exit or a count of collected tests is insufficient. An unresolved gold/rubric mismatch blocks that evaluation freeze. Revise targets, prompts, rubric or mutants prospectively in a new version based on the actual contract; never weaken an explicit requirement simply to obtain acceptance.

Changes to previously scored outputs/rules require a separately declared post-hoc sensitivity analysis, preserving the original scores. A frozen analysis of already-seen answers is not prospective confirmation. This gate supplements, and does not claim to complete, independent semantic review.

## Amendments and interruptions
Before execution, revisions remain draft history. After freeze, record any change with reason, timing and affected cells. Infrastructure-only reruns must preserve the original evidence and explain why a result is excluded. A changed prompt, decoding setting, token budget or repaired answer is a new condition, never a replacement first attempt.

## Notifications
Tell the observer when a study starts, completes, fails materially, or needs a decision. Explain question, finding and implication in ordinary language. Do not require the observer to referee routine implementation.

## Authorization
Reuse existing authorization where it covers the work. Ask only for genuinely missing scope or decisions, not repeated approval of the same corpus. Cloud spending, external publication, changing working apps/models, and opening reserved final evaluation are separate scope decisions.

## Publication readiness
Maintain exact provenance and environment, complete negative results, compute/time and memory costs, known review limitations, and a reproducible procedure. Before public release, review dataset/model redistribution permissions and local-path/private information. No publication is implied by preparing these documents.

