# Qwenny likelihood / generation gap investigation

Completed 2026-11-03 local time. No training was performed. Models, approved
training data and original results were preserved; final-test tasks were not used.

The gap is reproduced. E5 is substantially better at predicting the supplied
reference continuation, but neither removing the presence penalty nor using
greedy decoding produced a correct complete answer on these two development
tasks. This does not establish the cause of the gap or general model aptitude.

## Matched decoding result

Same instruction-only prompts, frozen base/E5, thinking disabled, 2,048 new-token
cap. Sampling uses seed 42, temperature 1, top-k 20, top-p .95. Presence penalty
is the custom output-only implementation described in METHOD.md.

| Decoder | Base strictly accepted | E5 strictly accepted |
|---|---:|---:|
| Sample, presence 1.5 (original first attempts reused) | 0/2 | 0/2 |
| Sample, presence 0 (new) | 0/2 | 0/2 |
| Greedy, presence 0 (new) | 0/2 | 0/2 |

Of eight new answers, three hit the output limit without a complete code block.
Four complete Python files failed against the correct implementation. The fifth
complete file failed parsing. None was reference-valid, so no mutant credit is
eligible. No answers were repaired or selected from retries. This is a small
three-condition comparison, not a full factorial experiment or pass-rate estimate.

Concrete failures:

- Base greedy rotation: 13 tests passed, 1 failed; rejects an ordinary tuple as
  though it were a subclass.
- Base sampled rotation: 14 passed, 4 failed; wrong wrapping/negative rotations
  and the same incorrect tuple rejection.
- E5 sampled rotation: 6 passed, 2 failed; wrong negative-rotation expectations.
- E5 greedy rotation: endlessly extends a huge integer and truncates; earlier
  expected results also contain arithmetic errors.
- Base sampled clock: 17 passed, 1 failed; invalid-type case tuples cannot be
  unpacked consistently. E5 sampled clock has a syntax error and also mixes
  valid/invalid inputs into None-return expectations.
- Both greedy clock answers truncate after excessive case enumeration. Base's
  unfinished source also contradicts itself about whether 01:59 is valid.

## What improved in the reference likelihood

Unpenalized teacher-forced NLL was reproduced within .005 of the original saved
development measurements. Lower is better; top-token accuracy below means
matching the next reference token when all prior reference tokens are supplied.

| Task | Base NLL | E5 NLL | Base next-reference-token accuracy | E5 accuracy |
|---|---:|---:|---:|---:|
| Rotation | .9278 | .3152 | 80.1% | 92.7% |
| Clock | .7862 | .0996 | 85.2% | 98.0% |

Approximate AST/source regions show why this average is insufficient:

- Prose/mapping plus the broad other-code region account for 97.1% of rotation's
  total NLL reduction and 87.7% of clock's. Other code includes executable logic
  and assertions; this is not a pure formatting measure.
- Rotation input-region NLL remains about .821 to .824, while expected-value
  region NLL increases from .123 to .202. These are only 135/60 reference tokens,
  and different valid examples may use different tokens.
- Clock E5 input-region NLL is .297, compared with .003 for expected values and
  .032 for other code. Thus a low average can conceal residual uncertainty in
  case construction.
- Applying presence 1.5 to the correct histories changes E5 NLL only from .315
  to .305 for rotation and .100 to .106 for clock. It is not uniformly harmful
  at those histories. Effects after divergent generated histories remain possible.
- Even under penalty-zero top-k/top-p filtering, 20 rotation and 7 clock reference
  tokens are excluded along the E5 gold history. This does not mean those positions
  necessarily cause errors: valid alternatives may exist.

These measurements support a distinction between learning a supplied continuation
and reliably constructing/completing a correct answer. They do not prove that
formatting alone was learned, that quantization caused failures, or that more
training would help. See INTERPRETATION.md for the next proposed ablation.

## Evidence and next step

- METHOD.md: exact scope and interpretation limits.
- RESULTS.json, likelihood-summary.json, likelihood/*/*/tokens.json: measurements.
- DV001/ and DV002/: all eight messages, outputs and generation records.
- ../../scoring/gap-001/: hash-reviewed reference/mutant execution and acceptance
  rejection reasons. Original penalty-1.5 outputs/scoring remain in their folders.
- SHA256SUMS.json: artifact hashes, regenerated after the report is complete.

Next prepare a separately versioned compact-target training ablation preserving
the substantive training cases/assertions and holding other training settings
fixed. Also keep a matched thinking-enabled base/adapted control on the agenda
before making claims about the original LM Studio workflow. No new training run
or target-format change was started during this investigation.
