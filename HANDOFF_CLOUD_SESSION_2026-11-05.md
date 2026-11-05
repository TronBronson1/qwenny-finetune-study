# Handoff: Claude Code cloud session, November 5, 2026

**For the next assistant (ChatGPT) and the user's PC.** Read this after `START_HERE.md`. It summarizes one long cloud session, and it does **not** replace `program/CURRENT_STATE.md`. When the PRs below are merged, update `CURRENT_STATE.md` and `START_HERE.md` in the project's usual style.

## Status at the end of the session

| Item | State |
|---|---|
| All work | On GitHub as **draft PRs**, none merged. Every PR adds files under new folders. |
| `CURRENT_CANDIDATE.txt` | Still `candidate-006`; nothing has changed it |
| Candidate-008 | Built and validated. **User-approved** hash `b65935295c94814fc7744f70feac49aedf809847a629961ae9bfbc75f72e18f4` (`dataset-v1/USER_REVIEW_2026-11-05.json`). |
| Candidate-009 (008 + error-path preservation) | Built and validated. **User-approved** wording and hash `a3f1425972bb5c25e8c9579ccad71b8f5555abc49f735cbe91d677f00b5b1aeb` (`dataset-v1/USER_REVIEW_2026-11-05-candidate-009.json`). It is the most complete candidate. |
| Training packets | Staged for both candidates, every row ≤ 2,048 tokens. **Neither is authorized for training.** |
| Training / GPU / model generation | **None** run in this session. Final/regression (EV/RG) content never read. |
| Adoption-rule pre-registration | Proposed, **not approved** |

Ready for training means **all** of these still have to happen, in this order:
1. The user states which candidate becomes current.
2. The user authorizes that candidate's packet hashes.
3. On the PC, the S009 diagnostic runs, then a maximum-example GPU preflight.
4. The pre-registration is approved before any held-out evaluation.

## Pull requests and merge order

| PR | Contents | Branch → base | Read first |
|---|---|---|---|
| [#1](https://github.com/TronBronson1/qwenny-finetune-study/pull/1) | Independent audit of candidate-007 gold suites (rubric mutants) | `claude/c007-rubric-audit` → `main` | `independent-review/c007-rubric-audit/REPORT.md` |
| [#4](https://github.com/TronBronson1/qwenny-finetune-study/pull/4) | Candidate-008 (study S010), TR058 fit overlay, staged packets, cloud gates | `claude/candidate-008` → #1's branch | `studies/S010-rubric-gap-repair/RESULTS.md` |
| [#6](https://github.com/TronBronson1/qwenny-finetune-study/pull/6) | Candidate-009 (study S011), read-through review, staged packets, approval record | `claude/candidate-009` → #4's branch | `studies/S011-error-path-preservation/RESULTS.md` |
| [#2](https://github.com/TronBronson1/qwenny-finetune-study/pull/2) | S009 slowdown forensics and the ready-to-run local diagnostic | `claude/s009-slowdown` → `main` | `independent-review/s009-slowdown/REPORT.md` |
| [#3](https://github.com/TronBronson1/qwenny-finetune-study/pull/3) | Power of the adoption rule, pre-registration proposal, `decide.py` | `claude/power-sim` → `main` | `independent-review/power-sim/REPORT.md` |
| [#5](https://github.com/TronBronson1/qwenny-finetune-study/pull/5) | This handoff | `claude/handoff-2026-11-05` → `main` | this file |

**Merge order:** #1 → #4 → #6 (stacked). #2, #3 and #5 are independent. GitHub retargets a stacked PR when its base merges.

## Decisions waiting on the user (record each one verbatim, tied to exact hashes)

1. **Current candidate:** 009 (recommended; approved, closes every audit gap) or 008. Changing `CURRENT_CANDIDATE.txt` needs an explicit statement.
2. **Training authorization** for the chosen candidate's staged packets, naming both hashes from its `report.json`:

   | Candidate | `messages_jsonl_sha256` | `train_jsonl_sha256` | Max row |
   |---|---|---|---|
   | 009 | `92c4a9c06ea950f78798be2e2a67c4d75761c721b6fb5fa4e0e24d87e80b5dbc` | `6b78f1cb87168675aaaa4a9ac505f2429c4e0e30fdfffb6fc83a1677c67cb0b2` | 1,967 |
   | 008 | `b3aa1c915a59937d7e67c0bfd4c03b6f1b09b7c48fb5817474078edb73fc4fbe` | `dd2eb1a02c9e64e0c2f0207bcc611125fba5d49ce0f15aa6a5d1ffd901d5e5e0` | 1,919 |

   The packets live in `studies/S011-error-path-preservation/packets-009/` and `studies/S010-rubric-gap-repair/packets-008/`. Each has `authorization.json` with `status: none`. Record a new authorization file rather than editing those.
3. **Pre-registration:** approve, or edit then approve, `independent-review/power-sim/PREREGISTRATION_PROPOSAL.md` before any held-out or regression generation. It includes an approval-record template.

## Next actions on the PC (in order)

From the repository root, in the existing `lora-feasibility` venv:

1. Optional: record this exact machine's validation for the chosen candidate.

   ```bash
   python studies/S011-error-path-preservation/validate_candidate_009.py --out studies/S011-error-path-preservation/validation-windows-pc
   ```

2. Fill in the S009 per-microbatch evidence from the local run folder, which is git-ignored. Each file is hash-checked.

   ```bash
   python independent-review/s009-slowdown/s009_forensics.py --run-dir training-v1/runs/qwenny-003-calibrated-baseline
   ```

3. S009 diagnostic: the CPU dry run first, then the real run. The real run takes ≤ 3.6 h and runs C0a, C1–C4 and C0b; C5 runs only after the user closes GPU apps and passes `--c5-confirmed`. Read `independent-review/s009-slowdown/diagnostic/PROTOCOL.md` first.

   ```bash
   python independent-review/s009-slowdown/diagnostic/run_diagnostic.py --dry-run --ceiling 60 --idle 1
   ```

   ```bash
   python independent-review/s009-slowdown/diagnostic/run_diagnostic.py
   ```

4. Before any training run: a new, separately frozen study with its own run IDs. It must include a maximum-example forward/backward preflight on the chosen packets: 1,967 tokens for 009, longer than the 1,880 S009 used, when S009 had only 0.2–0.4 GB of GPU memory free. Its time ceiling must have real headroom; S009's 1,200 s left only 6–11 %.

## What was done (short)

**1. Audit of candidate-007 (PR #1).**
- 1,134 single-requirement mutants were built from the unchanged references; 973 were confirmed different on a concrete input.
- The gold suites were run against all of them: 2,090 pytest runs.
- Surviving mutants: 121 in 006 → 76 in 007, 0 new.
- Remaining gap classes N1–N7:
  - N1: non-leading non-ASCII digits;
  - N2: ordinary wrong types that untyped code also rejects;
  - N3: no mixed type/value order witness;
  - N4: input mutation hidden by sorted inputs;
  - N5: boundaries;
  - N6: character preservation;
  - N7: error-path input mutation.
- Rerun or compare any pair:

  ```bash
  python3 independent-review/c007-rubric-audit/run_audit.py --candidates OLD NEW --results-dir DIR
  ```

**2. Candidate-008 (S010, PR #4).**
- **Build:** the builder reuses candidate-007's own builder functions after a gate that regenerates 911 candidate-007 files byte-for-byte. Additions for N1–N6 are declared in `repair_config_008.py`.
- **Size:** 1,555 gold cases; 463 designated mutants (all 407 from 007 plus 56 promoted from the audit).
- **Validation:** 72/72 suites on Windows (Python 3.15.2) and Linux.
- **Audit 007 → 008:** 76 → 19 surviving mutants, 0 new.
- **TR058 fit:** a presentation-only overlay (2,918 → 1,919 tokens) with the same AST and the same per-case results.
- **Known limitation:** TR030 case e013 is a weak type-before-shape witness, fixed in 009.

**3. Candidate-009 (S011, PR #6).**
- **Instruction change:** in the 19 mutable-input tasks, the coverage sentence becomes "Compare inputs before and after every call, including calls that raise." Every expected-exception test now checks its inputs, and 19 audit mutants are promoted.
- **Amendment 1, after a read-through review** (a fresh-context agent, not a human; `independent-review/case-review-008-009/`):
  - TR030 gets real type-before-shape witnesses plus a shape-first mutant;
  - DV001 adds "Compare arbitrary element objects by identity, not by copied value.";
  - three labels are renamed.
- **Result:** 1,557 cases and 483/483 mutants on Windows (Python 3.15.2). The audit leaves **0 of 973** confirmed mutants surviving, with none new. Total 64,384 tokens; the TR058 overlay is 1,967.

**4. S009 forensics (PR #2).**
- **Evidenced:**
  - The reconstructed batch order matches the logged totals exactly.
  - The stalled batch was TR031, a mid-length 1,188-token example; the longest examples had already completed seven times.
  - PyTorch's reserved memory never grew.
  - Other GPU consumers grew during the run; post-run usage exceeded what the load guard allowed at start.
- **Best-supported explanation:** external GPU consumers removed the headroom, followed by Windows paging. Paging is plausible but was not measured in S009.

**5. Adoption-rule power (PR #3).**
- At 24 tasks, a true +10 pp effect meets the ≥10 pp threshold only ≈45 % of the time.
- The "≤ 1 extra regression failure" guard falsely rejects a harmless adapter ≈20 % of the time.
- About 72 tasks are needed for 80 % power at +15 pp.
- The proposal uses a seed-pooled per-task estimand, an exact sign-flip test (one-sided 0.025), a three-way decision and a regression tolerance of 2.
- `decide.py` computes it, and `decide.py --self-test` checks it.

## Cloud gates (GitHub Actions, free for this public repo)

- `.github/workflows/s010-cloud-gates.yml` (branch `claude/candidate-008`) and `s011-cloud-gates.yml` (branch `claude/candidate-009`) run on each push to their branch:
  - Windows validation with Python 3.15 and pytest 9.2;
  - a pinned-tokenizer profile that must first reproduce the committed S007 profile;
  - staged packet preparation that must first reproduce S009's committed packets byte-for-byte, then commits its output once.
- Results are recorded in each study's `ci-run-*` folders and `RESULTS.md`.

## Rules to keep

- Never open, recreate or guess final/regression (EV/RG) tasks.
- Never modify existing evidence files. Add new files, studies or candidates, with hash manifests.
- Approvals and authorizations quote the user verbatim and name exact hashes. They never transfer to a changed file, and an approval of one thing (a hash) is not an approval of another (current candidate, training, pre-registration).
- Never train on failed development answers, and never repair inside a first-attempt score.
- The agent never closes the user's apps; the user does that (diagnostic condition C5).

## Environment notes

- The cloud session ran Python 3.13.18 / pytest 9.2.0 on Linux. Windows Python 3.15.2 checks ran on GitHub's runners, not on the user's PC.
- Hugging Face and GitHub artifact downloads were blocked from the cloud session. Tokenizer work therefore ran in Actions, and results were read from the job logs (`SUMMARY_JSON:`, `PROFILE_JSON:`, `REPORT_JSON:` lines).
- Generated mutant sources (`independent-review/c007-rubric-audit/build/`) and diagnostic dry runs are git-ignored and regenerated by the scripts.
