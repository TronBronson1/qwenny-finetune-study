# Qwenny study glossary

Updated November 4, 2026. The broader introductory glossary remains in [Report 001](REPORT_001.md). These terms explain the later calibration and controlled-training studies.

| Term | Plain-language meaning |
|---|---|
| Calibrated example | An example checked against the intended correct function and known defective versions using the same stated requirements. This is a finite check, not proof of every possible case. |
| Negative control | A deliberately inadequate answer or unrelated error that the measuring system must refuse to reward. |
| Reference-valid answer | Generated tests that finish, contain meaningful checks and pass against the intended correct function. They can still miss required behavior. |
| Strict acceptance | The complete answer meets the frozen correctness, required coverage, defect-detection, format and explanation rules. |
| Mutant | A deliberately defective version of a function, used to check whether a test detects a particular mistake. Several mutants can reflect closely related mistakes. |
| Witness | A concrete input and relevant failed check showing which defect was detected. A crash alone is not enough. |
| Input-bound scoring | Linking a claimed detection to the actual arguments and checks used by the generated tests, rather than relying on test names. |
| Verified calculation comment | A short visible note beside an example, such as `1*3+2 = 5`, checked against the contract, reference and separate calculation. It is authored explanation, not a recovered model thought process. |
| Paired training comparison | Two fresh training runs with matched starting adapters, randomness, example order and update count, while one planned aspect of the examples differs. |
| Fresh trajectory | Training starts again from the pinned base model and new initial adapter, rather than continuing an older adapter. |
| Supervised token | A piece of the authored answer that contributes to training error. Prompt text and the empty thinking wrapper are excluded in this study. |
| Answer mask | The record identifying which tokens contribute to training and which are ignored. |
| Preflight | A real small execution that checks memory fit, loss calculations, gradients and basic generation before the training updates begin. |
| Checkpoint import probe | Comparing a saved numerical output with the output after freshly loading the saved adapter. It checks that particular saved probe, not all possible behavior. |
| Code point / grapheme | A unit of Unicode encoding / a displayed character, which can contain more than one code point. |
| Unicode escape | Writing an encoding explicitly, such as `\u0301`, so a visually subtle character is preserved unambiguously in Python source. |
| Text normalization | A text-processing step that can change one Unicode representation into another visually equivalent one. That can change a literal code-point test. |
| Task-macro average | Calculate a fraction separately for each task, then average those fractions so a task with many cases does not dominate. |
| Prospective freeze | Recording the question, inputs, settings and scoring rules before observing the scored answers. Later clarifications must retain their actual timing. |
| Budget stop | Ending at a previously declared time or resource ceiling, even when the intended comparison is unfinished. |
| First attempt | The original generated answer under the declared settings. Failed, unfinished and malformed answers remain in the record. |

Training loss measures prediction of supplied answers. It does not replace checking freely generated answers, and no loss value alone selects a Qwenny upgrade.
