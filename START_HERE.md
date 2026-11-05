# Qwenny research program

Updated: November 4, 2026 (America/New_York).

Our goal is to test whether Qwenny can become more reliable on ordinary local hardware, and publish enough evidence and explanation for others to learn from the study. The first proof of concept is deliberately narrow: writing Python tests from precise function specifications.

**Current position:** local adapter training and fresh imports work; improved first-attempt correctness has not been demonstrated. No model has been selected. Final and regression evaluation remain reserved.

**Continue in a new chat:** read the [S009 stop handoff](studies/S009-value-comments/HANDOFF.md). The controlled comparison ended at its training-arm time ceiling. Its validated packets/scorer and partial baseline checkpoints are preserved; no comment-arm training or scored generation occurred. The next proposed work is a separately bounded resource/runtime diagnostic. No job is running.

**Important correction:** Independent review found gold answers that fail S006's own coverage rubric. The three cited mismatches are confirmed. Read [Report 003](observer/REPORT_003.md) before interpreting the older strict scores. S007 subsequently calibrated the revised corpus; original study evidence remains unchanged.

**Latest work:** S009 passed preparation, scorer calibration and both real hardware preflights, then its baseline stopped after 213 logged examples / 53 updates at the fixed 20-minute limit. E1/E3 are retained; no E5, paired quality finding or deployment. Read [Report 006](observer/REPORT_006.md) and [study results](studies/S009-value-comments/RESULTS.md).

## Read in this order

1. [Latest controlled-study report](observer/REPORT_006.md), [updated glossary](observer/GLOSSARY.md), then [introductory report](observer/REPORT_001.md). Reports 002–005 preserve earlier findings and review corrections.
2. [Current state](program/CURRENT_STATE.md): authoritative operational status.
3. [Study register](program/STUDY_REGISTER.md): completed work and its evidence.
4. [Roles and workflow](program/ROLES_AND_WORKFLOW.md): how work moves through review.
5. [S009 stopped-study results](studies/S009-value-comments/RESULTS.md), [S007 calibration](studies/S007-measurement-repair/RESULTS.md), and [S008 component results](studies/S008-fixed-input-values/RESULTS.md). The older training brief is historical; follow the S009 handoff for the next decision.

## Navigation rule

This page and program/CURRENT_STATE.md supersede obsolete present-tense status and next-step statements in older documents. Historical protocols, snapshots, outputs, hash manifests, and handoffs remain evidence of their original stage. Do not rewrite them to match later events.

No training, generation, deployment, or final-test access is triggered by these documents.

