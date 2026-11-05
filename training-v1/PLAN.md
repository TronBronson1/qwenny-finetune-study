# Qwenny controlled training v1

User authorized local training and multiple candidates after reviewing the corpus
and the successful 2048-token fit check. No cloud rental or app shutdown is part
of this run. Existing models, dataset snapshots and prior results remain intact.

## Fixed run, declared before training

Run: runs/qwenny-001. Three checkpoints from one deterministic trajectory at
epochs 1, 3 and 5, not three independently trained models. Differences measure
additional exposure on the same trajectory; they are not guarantees of differing
aptitude. Rank/scope/rate are not tuned in response to development results.

Base: Qwen/Qwen3.5-9B revision c202236235762e1c871ad0ccb60c8ee5ba337b9a.
Transformers 5.22.1, torch 2.14.1+cu126, PEFT 0.21.2, bitsandbytes 0.50.2,
Accelerate 1.15.0. NF4/double quantization and BF16 computation; frozen BF16 input
embedding explicitly on CPU, output head and transformer on CUDA. Non-reentrant
gradient checkpointing and 128-token checkpointed vocabulary loss.

Only q_proj/v_proj in eight full-attention blocks receive rank-4 / alpha-8 adapters:
557056 parameters, dropout zero. AdamW: learning rate 1e-4, betas .9/.999,
epsilon 1e-8, weight decay .01, gradient clip 1.0. Batch one, accumulation four:
60 microbatches and 15 optimizer updates per epoch; five epochs means 300 and 75.
First three optimizer updates linearly warm up to the fixed rate. Each microbatch
loss is normalized over its own supervised answer tokens, then divided by four.
No packing, padding or truncation. Seed 42; epoch shuffle uses Random(42+epoch).

## Data authorization and exact masking

The unchanged candidate-006 snapshot passed its hash-bound reference/mutant/oracle
checks. The user's corpus-level review and explicit training authorization are
recorded in ../dataset-v1/USER_TRAINING_AUTHORIZATION_2026-11-03.json. The export
accepts that explicit, exact-hash corpus approval without fabricating individual
reviewer actions. The original per-record approval route remains available; the
unapproved template and wrong-hash corpus approvals still fail. Check results:
export-authorization-checks.json.

Approved export: ../dataset-v1/training-approved-001. Prepared tokens:
prepared-001. All 60 complete training examples are <=1954 tokens. Supervision is
39730 assistant tokens out of 60552 input tokens per epoch. Every decoded supervised
span exactly matches the authored visible answer plus im_end. System/user text,
role headers, empty reasoning wrapper, and final formatting newline are ignored.

Training targets contain direct code answers plus mappings/limitations, not
fabricated reasoning traces. Inputs use the checkpoint's empty reasoning wrapper,
but there is no loss on its opening/closing thinking tokens. This choice does not
guarantee preservation of reasoning behavior. Historical LM Studio thinking-on
settings remain unchanged and require their own matched evaluation.

Tokenizer im_end=248046 and endoftext=248044; model config EOS is the latter.
Generation explicitly stops on either, avoiding a silent stop-token mismatch.

## Gates already implemented

- Full upstream file size/SHA256 verification before model load.
- Train/development-only ID checks and prepared-file hashes; no final or regression
  targets loaded into this training program.
- Mixed masked/supervised 64-token loss/gradient comparison against standard loss.
- Full longest-actual-example forward/backward, finite gradients and no base gradients.
- Short cached-generation compatibility check before optimizer training.
- Matched base development A/B teacher-forced losses recorded before updates.
- Every update checks finite/nonzero intended gradients and actual parameter change.
- Epoch 1/3/5 save includes adapter, optimizer/RNG state and a fixed reload probe.

Development controls use all 12 development targets, with instruction-only A and
two fixed original D01/D02 demonstrations B. Development target answers are used
only for no-gradient likelihood evaluation, never optimizer training. Mean
per-example loss is not strict executable task acceptance.

## Post-training checks

Fresh base loading and PEFT import of all three checkpoints must reproduce stored
probe logits. A secondary two-family generation pilot is prepared in
generation_probe.py: DV001 rotation and DV002 clock, base A/B and each adapter C.
Seed 42, temperature 1, top_k 20, top_p .95, and output-only presence penalty 1.5.
This pilot uses thinking disabled and a 2048-new-token cap for a separate,
bounded direct-answer check. Truncated outputs count as incomplete. It must not
be presented as the historical thinking-on, unrestricted-response comparison or
as formal final-test acceptance. The exact prompts, outputs, limits and timings
are saved. Formal category/prose review, broader regression and the untouched
24-task final test remain separate.

## Import/deployment boundary

Python module imports, cached inference, training and PEFT persistence are the
training-runtime compatibility checks. LM Studio's documented model import route
concerns GGUF model files; these PEFT adapters are not automatically standalone
LM Studio models. Merge/conversion/requantization and testing the deployed base
versus adapted model are a later compatibility stage. Do not overwrite the working
LM Studio GGUF or claim that deployment is already verified.

Primary documentation consulted:
https://huggingface.co/docs/transformers/training
https://huggingface.co/docs/peft/developer_guides/lora
https://lmstudio.ai/docs/app/advanced/import-model
