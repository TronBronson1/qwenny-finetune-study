# S009 — verified value comments

Prospective protocol, November 4, 2026 (America/New_York). Frozen by the accompanying SHA256 manifest before GPU preflight, training or new scored generation. Routine local execution is authorized by the user's “Perfect you may proceed with the plan.” No claim is made that the user reviewed the exact newly authored comments.

## Question and variants

Do short verified value calculations improve first-attempt pytest generation relative to an otherwise identical calibrated training corpus? Three inference arms: pinned base without adapters; fresh calibrated baseline E5; fresh comment-treatment E5. E1/E3/E5 are saved and import-checked for provenance; E5 alone is the endpoint. No checkpoint selection from loss or generated answers.

The two 60-record training exports derive from candidate-007 with the certified complete TR058 overlay. Twenty-three normal-return rows across TR007 (digit sum), TR010 (set-bit positions/count), TR038 (hex positional value) and TR049 (row-major offset) receive comments in the treatment only. Families were selected from contracts before new model output. Each expression equals the stored expected value, independent valid-domain oracle and unchanged reference. No failed development answer is a target. Comments are visible authored calculations, not hidden model reasoning.

TR049 optional comma spacing is removed in both arms; executable AST stays exact. All other source changes are comments and the already certified TR058 display/presentation overlay. Cases, assertions, prompts, order and splits remain matched. Neither original candidate is overwritten. Exact exports and per-record provenance are in preparation-001. Baseline/comment totals per pass: 61,313/61,677 input tokens and 42,255/42,619 supervised tokens. Maximum chats: 1,880/1,920. Fixed updates do not equate token exposure or FLOPs. Treatment adds 364 supervised tokens per pass, 1,820 across five passes (about 0.86%).

## Preparation, authorization and gates

Exact variant hashes are recorded in preparation-001/authorization.json using the current delegation, without inheriting candidate-006's approval. Missing, wrong-hash and changed prepared data must be rejected. All training IDs are TR001–TR060, same order. Twelve development targets retain historical instruction-only A and fixed D01/D02 demonstration B no-gradient loss views: 24 rows, never optimizer inputs. The DV008 development target represents its combining accent with a literal Unicode escape, with exact AST equality; raw combining text is normalized by the tokenizer and fails exact decoding. Both arms use the same escaped loss target. No development expected value changes.

Every supervised decode must equal the visible answer plus im_end; prompts, roles, empty thinking wrapper and final formatting newline are masked. No truncation, packing, silent context expansion or fabricated duplicate development rows.

Before GPU allocation: verify all original source hashes; exact packet expression and AST checks; execute both 60-target variants against references and every designated mutant; calibrate the model scorer on all eight selected gold suites under the same requirements/eligibility rules and negative controls. Gold calibration is finite and same-agent, informed by parent external review; it is not independent semantic sign-off.

Before either optimizer trajectory: separate full-longest-example forward/backward checks for both packets; mixed masked standard/chunked loss agreement below 0.001 absolute and gradient relative L2 below 0.03; finite intended adapter gradients and no frozen-base gradients; cached greedy smoke test terminating within 24 tokens; no-gradient development controls. Both fresh initial adapter parameter hashes must match. Actual runs must match those initial hashes and begin from the same saved seed state, with no resumed weights.

## Fixed training/runtime

Qwen/Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a; existing locked local runtime: torch 2.14.1+cu126, Transformers 5.22.1, PEFT 0.21.2. Existing NF4/double quantization, BF16 compute, frozen CPU input embedding, CUDA transformer/head/adapters, gradient checkpointing and chunk-128 masked loss. Only q_proj/v_proj in eight full-attention blocks: rank 4, alpha 8, dropout 0, 557,056 trainable parameters.

Seed 42; fresh adapter and RNG state matched. AdamW lr 1e-4, betas (0.9,0.999), epsilon 1e-8, weight_decay 0.01, clip 1. Batch 1, accumulation 4; first three updates warm up; five passes, 300 microbatches, 75 updates. Per-example target-token-normalized loss divided by four. Epoch order Random(42+epoch). Initial adapter hash and initial CPU/CUDA RNG fingerprints recorded. Base gradients prohibited. E1/E3/E5 save adapter, optimizer/RNG and reload probe. Actual fresh-import max absolute logit difference must equal 0, the existing demonstrated criterion; save observed differences and stop on any mismatch. Do not relax tolerances after a failure.

## Matched first attempts

Task order: TR024, DV008, TR025, DV004, TR038, DV011, TR049, DV007. Rotate base/baseline-E5/comments-E5 order by task index modulo three. One attempt per arm/task: 24 planned. Identical candidate-007 system/user prompts in all arms, direct-answer empty thinking wrapper. DV008 adds explicit Python Unicode-code-point/no-normalization wording prospectively in all inference arms. This differs from historical S006/S008; no single-factor comparison to those studies.

Seed 42 reset each cell; temperature 1, top_k 20, top_p 0.95, presence 0, repetition 1; 2,048 new tokens, total context 16,134; stop IDs im_end 248046 and endoftext 248044. Save exact rendered prompts and IDs, first outputs and partials, raw tokens, times, memory and stop reasons. No repair, retry, best-of-N or replacement of a failed attempt. A later scorer infrastructure correction may re-execute identical saved source, preserving the failed execution and documenting the cause; never regenerate an answer to repair it.

## Measures and source review

Primary: reference-valid first attempts out of all eight planned tasks per arm, separately four familiar training and four development tasks. A first attempt must complete, present one executable Python block, collect at least one meaningful contract assertion/test call, and pass the reference with no failure/error/skip. Mere call-only/vacuous/empty suites do not qualify. Unattempted or truncated answers remain failures in the planned denominator. Also report raw reference execution results separately from meaningfulness/format/completion exclusions.

Secondary: completion, syntax/collection, requirement evidence, mutant detection and strict calibrated acceptance, plus prose. Review every generated source before bounded subprocess execution, bind approval to exact source SHA256, inspect imports and prohibited replacement/introspection/side effects, and record exclusions. The automated AST guard supplements human-agent inspection; it is not a security sandbox or semantic proof.

The scorer instruments actual function calls per generated test node. It compares actual arguments/outcomes/post-state with the trusted reference on copied inputs. Candidate mutant detections require a failing assertion on a return/post-state discrepancy; a missing required exception; or a declared related TypeError/ValueError/IndexError mismatch on contract-invalid input. Valid-input crashes, setup/collection failures, timeouts and unrelated errors earn no credit. Never match arbitrary model node names against gold node IDs. Review/hash-bind each eligible failure to its actual model inputs and relevant contract requirement; trace candidates alone are not final credit. No mutant credit for reference-invalid suites. Report task-level ratios over all designated fixtures only among reference-valid tasks and average those ratios per task; show the eligible-task count and descriptive planned-denominator zeros separately.

Requirement review uses each selected rubric's semantic categories and explicit contract: ordinary values, every specified argument/nested type level with ordinary wrong types and subclasses/bool where required, invalid domain/shape/bounds, validation priority, exact output type/structure, nonmutation/order where specified. Equivalent witnesses are allowed; matching gold examples or test names is not required. Record per-requirement evidence or absence and task-macro fraction. Strict acceptance requires primary reference validity, all applicable explicit requirements supported, all designated mutants eligibly detected, instruction-conforming output and correct mapping/limitations prose with no fabricated execution claim. Report these layers separately. The same criteria are applied to selected calibrated gold during prospective calibration; historical S006 scores remain unchanged.

Prose review records unsupported execution claims, mapping truth, explicit finite-coverage limitations and any misleading assertions. Do not silently credit keyword presence as semantic coverage.

## Ceiling, stopping and interpretation

One local GPU owner. Three-hour total GPU orchestration wall ceiling including verification/loading/preflights, training and inference; each preflight at most 600 seconds, each training arm at most 1,200 seconds, inference at most 7,200 seconds within remaining global budget and each generation cell at most 300 seconds. Whole frozen orchestration stops at the first failed prerequisite, nonfinite result, wrong initial state, import mismatch, memory guard or timeout. Preserve partials and unattempted cells. At least 8 GiB CUDA free required at every fresh model load. No cloud, app closure, persistent power changes, working-model replacement, merge/conversion, LM Studio automation or final/regression content access. Process-scoped keep-awake ends when its process exits.

Record wall time and token costs, GPU allocated/reserved peaks and driver memory samples. Report unavailable Windows process-memory evidence as unavailable; do not infer shared-memory spill.

With four familiar/four development purposive tasks and one seed, report paired task outcomes and counts descriptively; do not treat correlated cases/mutants as independent trials or claim population significance. A better treatment reference-valid count without lost requirement coverage motivates a frozen broader development confirmation, not selection/deployment. Ties, conflicting measures, budget failure or narrow familiar-only benefit are inconclusive; worse outcomes oppose this treatment under these settings. No winner from falling loss alone. Any adoption still needs strong prompted-base, frozen seed/task aggregation, uncertainty and regression/reserved evaluation.

At completion preserve results/costs/limitations, write Observer Report 006 and glossary updates, update START_HERE, current state, study register, decisions and backlog. No adapter is selected or deployed by this study alone.
