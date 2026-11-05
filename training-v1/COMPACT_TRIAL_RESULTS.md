# Compact-target trial 001 results — 2026-11-04

The presentation-only training ablation is complete. Three additional experimental
adapters are saved and fresh-import verified. The predeclared E5 pilot remains
0/2 accepted: both generated files have syntax errors. Shortening the targets did
not close the likelihood/free-generation correctness gap in this small pilot.
This does not establish the effect on other tasks or seeds.

## Data preservation and controls

Same 60 reviewed training tasks, prompts, order and splits. Removed pytest display
IDs/blank lines/trailing spaces and shortened repeated mapping/limitations prose.
No executable AST changed except display IDs: all arguments, expected values,
assertions, exception checks and helpers were preserved. Original files remain.

Paired execution of original and compact targets on 60 correct implementations
and 180 designated mutants produced identical per-test-function outcomes across
240 pairs (480 pytest processes). All 1,035 reference test cases pass in the
compact version. The development tokenized targets are byte-identical to the
original prepared data. No final-test or regression targets were used.

Supervised tokens fell from 39,730 to 30,660 (22.83%). Total input tokens fell
from 60,552 to 51,482; maximum complete input from 1,954 to 1,578. No truncation.
The experiment bundles presentation changes; it does not isolate their effects.

## Training and import

Fresh same pinned Qwen3.5-9B base, seed42, rank4/alpha8, same attention q/v scope,
NF4/BF16 CPU-embedding runtime, batch1/accumulate4, learning-rate/warmup/optimizer/
clip/shuffle settings unchanged. The trainer matches the first run byte-for-byte;
model/loss runtime definitions match structurally. Only temporary keep-awake
monitor lifecycle differs. All base pre-update development losses match exactly.

Five passes, 300 examples, 75 optimizer updates; each task seen exactly five times.
Training plus checkpoint development evaluation took 608.281 seconds (~10.1 min),
excluding loading/preflight/base controls and generation. Equal examples/updates
does not mean equal token exposure or compute.

Training-stage peak allocated GPU memory: 7,280,687,104 bytes (~6.78 GiB), reserved
8,095,006,720 bytes (~7.54 GiB); minimum sampled stage free CUDA memory
801,038,336 bytes (~764 MiB). Windows process shared memory peaked at 85,983,232
bytes (82 MiB) during the training interval. Other application usage can affect
headroom; these are measurements from this run, not a universal fit guarantee.

All saved E1/E3/E5 adapters reproduced stored probe logits with maximum absolute
difference 0.0 when reloaded in a fresh process. They are PEFT adapters, not
standalone GGUFs, deployment-tested models or tiers of aptitude.

## Predeclared generation pilot

E5 only; same DV001/DV002 instruction-only messages, thinking disabled, seed42,
temperature1/topk20/topp.95, presence0/repetition1, cap2048/context16134, explicit
stops. One first attempt per task. No repairs, retries or checkpoint selection.
Full source reviewed and hash-bound before unchanged reference/mutant execution.

| Task | Original E5 sample0 tokens | Compact E5 sample0 tokens | Original accepted | Compact accepted |
|---|---:|---:|---:|---:|
| Rotation | 520 | 530 | No | No |
| Clock | 931 | 537 | No | No |

Neither compact answer truncated. Both returned one closed Python block and
brief prose, but failed parsing before any tests could run:

- Rotation: mismatched parentheses in a nested tuple case. Source also gives
  wrong results for rotation by +/-4 and omits the steps argument in some
  type-check cases. An arity TypeError would not demonstrate exact-type rejection.
- Clock: mismatched parentheses in exception parameters. Source also corrupts
  parameter tuple structure, ignores the function return when comparing values,
  and puts malformed strings under the wrong exception class.

No reference-valid answer means no eligible mutant-detection credit. Syntax fixes
were not applied to rescue these first attempts. The clock answer was shorter;
rotation was slightly longer. No reliable length or accuracy improvement follows
from two visible families and one seed.

## Secondary loss diagnostic

Development answers remain in the original format. Mean per-example A/B losses:

| Stage | Original run A / B | Compact run A / B |
|---|---|---|
| Base | .89338 / .78991 | .89338 / .78991 |
| E1 | .76984 / .70822 | .80625 / .72668 |
| E3 | .38160 / .43057 | .56971 / .52678 |
| E5 | .13293 / .22185 | .54489 / .49732 |

Compact training loss declines to .12260 on its own format; this cannot be directly
compared with old-format training loss. Common-target development loss favors the
original presentation and is sensitive to that presentation. Neither loss table
establishes correct autonomous test generation.

## Artifacts and next investigation

- COMPACT_TRIAL_PLAN.md: protocol recorded before training and generation.
- prepared-compact-001/: transformed messages, targets, masks and provenance.
- validation-compact-001/: all paired execution logs and outcomes.
- runs/qwenny-002-compact/: trainer, snapshots, checkpoints, events, memory logs.
- candidates/qwenny-002-compact/: three separately packaged adapters and hashes.
- probes/qwenny-002-compact-sample0-001/: original messages, both first answers,
  fresh-import checks and code inspections.
- scoring/qwenny-002-compact-sample0-001/: unchanged evaluator logs and explicit
  rejection review. compact-trial-results.json links the machine-readable result.

Preserve all candidates without adopting a winner. Next useful control is matched
thinking-enabled base/adapted inference before more training or claims about the
historical LM Studio workflow. That control has not yet run. No causal conclusion
about 4-bit precision, long-cache behavior or general aptitude is justified.
All GPU jobs from this trial have finished; no LM Studio models/settings changed.
