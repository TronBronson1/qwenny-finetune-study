# What the learning-and-transfer diagnostic found

Report 002 • November 4, 2026

**We completed the study. We can run and verify Qwenny's adapters on the local RTX 3080, but this experiment still does not demonstrate reliable improvement in writing tests.**

The useful new finding is that failure was not simply caused by running out of space or encountering unfamiliar problems. All 24 answers finished, and clear mistakes also appeared on training specifications the adapters had seen before.

## What we asked

Could trained Qwenny write correct tests for familiar problems? Would its behavior differ on development problems?

We chose four familiar training tasks and four development tasks using a fixed rule spanning short and long supplied answers. We tested the original model, the checkpoint after one training pass (E1), and the checkpoint after five passes (E5). That produced 24 first attempts.

The familiar tasks involved ASCII uppercasing, run-length encoding, reading a hexadecimal byte, and indexing a grid. Development tasks involved edit distance, XOR checksums, merging intervals and finding grid neighbors.

No new training occurred. No answer was repaired or retried.

## What happened

| Task group | Model | Passed the correct function | Passed it and met all 3 designated-defect checks | Met every requirement |
|---|---|---:|---:|---:|
| Familiar training | Original base | 2/4 | 2/4 | 0/4 |
| Familiar training | E1 | 3/4 | 2/4 | 0/4 |
| Familiar training | E5 | 1/4 | 0/4 | 0/4 |
| Development | Original base | 1/4 | 0/4 | 0/4 |
| Development | E1 | 0/4 | 0/4 | 0/4 |
| Development | E5 | 1/4 | 1/4 | 0/4 |

These small counts do not identify a winning checkpoint. E1 and E5 are saved stages from the same training run, not independent attempts at training.

Eight suites passed the correct function. Five also met the frozen evaluator's all-three-defect rule. None satisfied every required specification category.

## Why an answer can work and still fall short

Suppose a contract says to reject a custom subclass of a string. A suite can test ordinary strings perfectly but never try a subclass. It may pass the correct implementation while letting a defective one through.

Another contract requires an exact built-in integer result. Checking that a result is broadly an integer can also accept an integer subclass. A meaningful exact-type check needs to distinguish those cases.

These requirements were part of the study before the answers were generated. We did not add them afterward to turn a success into a failure.

Some answers had more basic errors. E5's uppercase example left a lowercase letter unchanged. Its grid-offset example expected 4 where the correct answer was 3. Other answers supplied the wrong number of arguments, chose the wrong exception type, or constructed invalid pytest syntax.

A polished explanation did not guarantee that the concrete test cases were right.

## What we can conclude

We have established local training and adapter-loading feasibility. We have not established a useful first-attempt accuracy improvement for this task.

Because all answers finished, giving these same attempts more output space would not explain away their recorded errors. Because errors also appeared on familiar specifications, the problem is not confined to transfer.

We cannot conclude that all fine-tuning is ineffective, that E1 is generally best, that 4-bit precision caused the mistakes, or that a larger GPU would fix them. This study used one seed and eight deliberately selected tasks.

It also did not compare an adapter with the original model plus demonstrations, which remains part of the original practical question. The protected final and regression evaluations remain reserved.

## What it cost

The model-loading, verification and generation process took about 54 minutes. The 24 generation cells used 27,105 output tokens. CPU evaluator checks and report preparation took additional time.

Peak measured Torch memory was about 7.38 GiB allocated and 7.44 GiB reserved. The lowest sampled free GPU memory was 692 MiB. This was tested on the local 10 GB RTX 3080; it is not a minimum specification for every computer.

The Windows per-process memory sampler produced no usable samples, so we cannot say whether the process used shared GPU memory. All jobs finished, and the temporary keep-awake request ended.

## How trustworthy is this?

We checked the adapters against their saved measurements, matched prompts across models, retained all first attempts, ran actual tests and checked file fingerprints. The final integrity checks passed.

There are still review limits. The coordinating agent performed the source and coverage review; this was not independent scientific validation. One grid specification could state its outer container more clearly. The scorer also has a conservative rule about unexpected exceptions, which may exclude some meaningful defect symptoms. Both issues are documented, and the original results are preserved.

A worthwhile study should make those limits inspectable.

## What I recommend next

**Review the task, prompt and scoring design before spending more GPU time on training.**

A separate reviewer should check the eight task contracts, correct answers and designated defects; clarify ambiguous wording and exception-credit policy; and inspect whether general instructions introduce irrelevant ideas. For example, guidance about reversed bounds appeared in explanations of a string parser.

After that audit, we can design one small change aimed at a specific observed failure. We should preserve the original study and compare any revised approach fairly with the unchanged base. More epochs alone are not yet an evidence-backed next step.

## A few new terms

| Term | Plain-language meaning |
|---|---|
| Familiar-example check | Asking about a training problem. Useful for diagnosis, but not proof of transfer. |
| Purposive sample | Tasks selected by a declared rule for a purpose, rather than randomly sampled from a population. |
| Arity | The number of arguments a function expects. A wrong-arity error can make a supposed validation test meaningless. |
| Equality versus identity | Equal values need not be the very same object. A test should demand identity only when the contract requires it. |
| False alarm | A generated test rejects a correct implementation, often because its expected answer is wrong. |
| Semantic review | Checking whether the words, examples and scoring actually mean what we intend, beyond whether software runs. |
| Diagnostic study | A study meant to identify the next question or intervention, rather than confirm a final improvement claim. |

For the longer glossary, see [Report 001](REPORT_001.md).

## Explore the evidence

- [Technical results and every first attempt](../studies/S006-learning-and-transfer/RESULTS.md)
- [Interpretation and next decision](../studies/S006-learning-and-transfer/INTERPRETATION.md)
- [Execution review](../studies/S006-learning-and-transfer/EXECUTION_REVIEW.md)
- [Current program state](../program/CURRENT_STATE.md)

A question to consider: if a suite catches all three planted bugs, why might it still miss an explicit requirement? The planted bugs are a finite sample of defects; passing those checks does not establish complete specification coverage.

