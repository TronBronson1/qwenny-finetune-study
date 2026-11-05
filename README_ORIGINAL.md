# Qwenny: coding accuracy experiment

> **Current navigation — November 4, 2026:** Start with [START_HERE.md](START_HERE.md), the [current state](program/CURRENT_STATE.md), and the [observer report and glossary](observer/REPORT_001.md). Local training, compact-target training, and the thinking-enabled control are complete. No strict quality gain or winning candidate has been established; final and regression evaluation remain reserved. The text below is the historical project introduction; its pending milestones and “no training” statements describe earlier stages, not current status.

Started November 3, 2026. Status: experiment designed; no training or model evaluation performed here yet.

## Question

Can a small LoRA adapter make Qwenny more reliable at writing Python tests than a strong prompt with examples?

Our first target is deliberately narrow: given a precise function specification, write a pytest suite that accepts a correct implementation and detects implementations with planted defects. General coding challenge solving is a later extension. Keeping one task type makes the first result easier to interpret.

## Start here

1. Read `01_EXPERIMENT_PLAN.md` for comparisons, scoring, and success criteria.
2. Read `02_MACHINE_AND_TRAINING.md` for hardware and the separate Ollama inventory. Use `04_LM_STUDIO_BASELINE.md` for the active LM Studio pilot settings documented from screenshots.
3. Use `pilot/PROMPT.md` in a fresh Qwen chat for the first development task. This is a workflow rehearsal, not a held-out result.
4. Save the full request, response, settings, and actual execution results under a new directory in `runs/`. Use `runs/RESULT_TEMPLATE.md`.
5. Build and review task families using `03_DATASET_RULES.md` before any training.

## What we already learned

The previous discount-testing experiment showed that Qwenny could repair its tests after concrete execution feedback. The corrected suite passed the reference and detected the planted string-percentage bug, while its prose still overstated completeness. That is evidence for feedback-assisted repair on one task, not a training result or proof of broad reliability.

Source: `../Python Testing/EXPERIMENT_SUMMARY.md`. Earlier plans: `../Qwen Training Learning Plan - 2026-10-27.md`. Those files remain unchanged.

## Learning map

| Term | What changes in this experiment |
| --- | --- |
| Prompt/context | Instructions and examples supplied for a request |
| Weights | Learned numerical parameters of the model |
| Quantization | Numerical precision/representation of model parameters |
| Fine-tuning | Further training using reviewed examples |
| LoRA | Trainable weight updates added while the base weights stay frozen |
| QLoRA | LoRA training with a quantized base; distinct from simply running an Ollama GGUF |

LoRA background: [Hugging Face PEFT](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora). Quantized adapter training: [PEFT guide](https://huggingface.co/docs/peft/en/developer_guides/quantization).

## Immediate next milestone

Complete the development pilot, verify the reference and planted bugs, and establish a repeatable scoring workflow. Then assemble the split dataset and measure the two prompting baselines. Choose and test the training stack only after this foundation is working.

## Next experiment: demonstrations

See 06_DEMONSTRATION_COMPARISON.md. Two checked demonstrations are saved in prompt-comparison/DEMONSTRATIONS.md with execution logs. Keep the current system prompt and settings fixed; score new-task first attempts and one-repair outcomes separately. LoRA remains the first planned weight alteration. Qwen A/B comparison results are still pending.

## Completed prompting development check

See prompt-comparison/COMPARISON_RESULTS.md for the completed two-task comparison. First attempts: A 0/2, B 0/2. After one repair: A 1/2, B 0/2. No demonstration benefit observed in this small pilot. Next milestone: LoRA compatibility and memory-fit trial in 02_MACHINE_AND_TRAINING.md. No weight training has been performed.
