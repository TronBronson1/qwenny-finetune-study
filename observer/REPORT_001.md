# Qwenny lab notebook for the observer
Report 001 • November 4, 2026
Purpose: understand whether we can improve a local model on ordinary hardware, while learning how to conduct a study others can inspect and enjoy.

## The question in everyday terms
We ask Qwenny to read a precise description of a small Python function and write tests for it. Good tests should accept a correct function and catch specific broken versions. We want to know whether a small amount of training makes Qwenny more reliable than simply giving the original model good instructions and examples.

That is our first proof of concept. Success would support a narrow claim about writing these tests under measured conditions. It would not establish that Qwenny became better at every kind of programming.

## What we have achieved
We can train small add-on weight files on the local RTX 3080, save them, and load them again with matching verification measurements. We have created tasks, checked correct and intentionally broken implementations, and kept experimental evidence.
This is an engineering proof of feasibility.

We have not yet demonstrated the second proof: that trained Qwenny reliably produces better complete answers on new problems.
The most recent thinking-enabled comparison tested the original model and two trained variants on two development tasks. Each scored zero out of two under the full acceptance rules. Five of the six answers ran out of allowed output tokens. Negative results are useful when they are preserved and interpreted honestly.

## Why a better training score can still mean a bad answer
Imagine completing a worksheet with the teacher supplying every correct word up to the next blank. You may predict the next word well. Writing the whole answer alone requires you to choose the path and recover from your own mistakes.

Our training measurements resemble the first situation. Ordinary generation resembles the second. Training made the model better at predicting supplied answers, but that did not guarantee correct independent construction.

## What “thinking” means here
Thinking-enabled mode produces extra reasoning text before a final answer. It consumes time and tokens. More reasoning text does not guarantee a correct answer. In the latest bounded study, it often consumed the available allowance before producing a final answer.
The earlier direct-answer study used a smaller allowance, so comparing those studies does not isolate the effect of thinking alone.

## What happens next
First we organize the program and review a diagnostic study. The proposed study asks whether trained Qwenny can write correct tests for familiar training problems, then compares that behavior with development problems.
If it works on familiar problems but fails on development problems, transfer deserves attention. If it fails on both, we should inspect alignment and answer construction before adding more training. If outputs mainly run out of space, completion deserves a separately designed study.

The proposal is not a completed experiment or a promise of improvement. Its exact tasks, resource budget and review still need to be settled.

## Your place in the lab
You provide the purpose, curiosity and practical priorities. You do not need to choose technical settings or judge Python syntax. The team should bring you short explanations of the question, findings, uncertainty and recommended decision.
You should hear about meaningful starts, completions, failures and decisions. You should not need to reconstruct progress from logs.

## A useful way to read future reports
Ask: What changed? What stayed matched? Were the tasks familiar? Did the full answer work? Were failed attempts retained? Does the conclusion reach further than the evidence?
A result can be technically interesting without being an improvement. A small study can suggest the next question without settling the main one.

## Glossary
| Term | Meaning in this project |
|---|---|
| Base model | The starting model before our adapter is added. |
| Weights | Numbers that determine how the model transforms its input into predictions. |
| Fine-tuning | Further training that changes selected learned weights using examples. |
| LoRA / adapter | A relatively small set of trainable additions used with the original model. It is not a standalone complete model. |
| QLoRA | Training adapters while the base model is held in a reduced-precision form. |
| Quantization | Representing model numbers with fewer bits to reduce storage or memory. Its effect on our failures has not been isolated. |
| NF4 / BF16 | Numerical formats used in this local training setup: a compact base representation and a computation format. |
| GPU / VRAM | The graphics processor and its dedicated memory. Memory capacity constrains what we can run locally. |
| Inference / generation | Using a model to produce an answer rather than train it. |
| Prompt | Instructions, examples and task text supplied to the model. |
| Token | A chunk of text processed by the model; it may be a word, part of a word, punctuation or code. |
| Context window | The capacity available for the input and generated continuation. |
| Token cap / truncation | The maximum allowed generated length / an answer stopping because it reaches a limit. |
| Epoch | One pass through the training examples. |
| Checkpoint | A saved model or adapter state from a particular training stage. E1/E3/E5 come from one trajectory. |
| Loss | A numerical prediction-error measure. Lower loss on supplied answers does not establish correct generated code. |
| Teacher forcing | Measuring or training the next prediction while supplying the correct previous answer tokens. |
| Training set | Examples used to update adapter weights. Success here does not demonstrate transfer. |
| Development set | Problems used to investigate and choose approaches. Repeated use makes them unsuitable as a final untouched test. |
| Final / held-out set | Reserved problems used after choosing and freezing the approach. |
| Regression test | A check that a change has not damaged other behavior we care about. |
| Reference implementation | The intended correct function against which generated tests are run. |
| Oracle | A separate way to determine expected behavior for checking the reference or examples. |
| Mutant | An intentionally defective implementation used to see whether a test catches a particular bug. |
| pytest | The Python tool that runs the generated test suites. |
| Collection error | Failure while pytest loads/discovers tests, before it can run them normally. |
| Reference-valid | Generated tests pass against the correct implementation. This alone does not prove adequate coverage. |
| Coverage | Meaningful checks of the specification's required cases; test names alone do not establish it. |
| Strict acceptance | Meeting all frozen requirements, including correctness, required defect detection, coverage and format. |
| Seed | A setting used to control random choices; it is not a guarantee of identical behavior across different software/hardware. |
| Temperature / top-k / top-p | Settings controlling how candidate next tokens are sampled. |
| Presence penalty | A decoding adjustment that discourages repeating tokens already generated. |
| Baseline / arm | A reference condition / one condition in a comparison. |
| Ablation | A study that changes or removes a particular factor to investigate its effect. |
| Confound | Another difference that prevents a comparison from isolating the factor of interest. |
| Generalization / transfer | Applying learned behavior to problems beyond the training examples. |
| Data leakage | Information crossing a boundary that makes evaluation less trustworthy, such as training on final answers. |
| Protocol / freeze | The planned experiment / locking its relevant choices before seeing results. |
| Hash / provenance | A file fingerprint / the record of where data, code and results came from. |
| Reproducibility | Providing enough exact information for someone to repeat the procedure and assess the findings. |
| GGUF / deployment | A model-file format used by local runtimes / putting a candidate into its intended working application. |

## Learning prompts for between studies
1. Why might passing the correct implementation be necessary before counting caught bugs?
2. Why would choosing the best of ten attempts answer a different question from first-attempt reliability?
3. Why is “we can train it” different from “training improved it”?
4. Why should final questions remain reserved until we choose our approach?

Suggested answers: broken tests may reject everything; extra attempts add selection and cost; engineering feasibility and behavioral benefit require different evidence; choosing based on final results turns that evaluation into development.

## Evidence and further reading inside this project
- [Current state](../program/CURRENT_STATE.md)
- [Study register](../program/STUDY_REGISTER.md)
- [Original research question and acceptance rule](../01_EXPERIMENT_PLAN.md)
- [Latest thinking-control results](../training-v1/THINKING_CONTROL_RESULTS.md)
- [Next diagnostic proposal](../studies/S006-learning-and-transfer/PROTOCOL.md)

This report describes local project evidence. It makes no broad claim that training helps or harms all models. Next report: the reviewed S006 outcome, if executed, including negative and incomplete results.

