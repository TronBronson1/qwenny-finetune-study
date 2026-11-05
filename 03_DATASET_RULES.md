# Dataset construction and leakage rules

Assign a family ID and split before writing variants. Split by underlying function/problem family, not random rows. Renaming discount to rebate, changing constants, or paraphrasing a prompt does not create an independent held-out family.

## Record per task

- Stable task ID, family ID, split, author/source, and revision.
- Exact specification and model-visible import contract.
- Correct reference, independently checked acceptance cases, and explicit invalid inputs.
- Single-defect mutants with intended witness inputs and why they violate the contract.
- Reviewed target pytest file and a short honest limitation statement.
- Execution evidence, Python/pytest versions, and reviewer notes.

Create simple numerical, string, collection, parsing, and indexing tasks. Include boundaries, exact type rules where specified, exception contracts, and valid nontrivial examples. Avoid undefined behavior, huge-number ambiguity, external dependencies, or conflicting contracts in the first collection.

## Training targets

Prefer explicit argument tuples and clear expected results over conditional argument construction. Each invalid-input test should hold other inputs valid unless the contract explicitly requires mixed-invalid behavior. Assertions must check results or specific exception types; merely calling a function is insufficient.

Train on reviewed successful outputs, not raw model answers. If including repair examples, keep the initial faulty response, actual execution feedback, and corrected response as a separate labeled task type. Do not accidentally teach the faulty answer as the target.

Use a chat-message JSONL format only after selecting the trainer and confirming its expected schema. Keep source task records independent of the trainer format. Record licensing/provenance and remove personal or secret data.

## Quality gate

Every target suite must pass the reference and detect its designated mutants through meaningful failures. Run an independently written oracle check against the reference as well: generated tests passing a mistaken reference do not validate it. Review argument pairs manually for the earlier conditional-argument bug pattern.

Keep development prompts, demonstration choices, and checkpoint selection away from final-test families. Demonstrations come only from the training split and remain fixed across tasks. Never use final evaluation answers or mutants in training. Hash the frozen dataset and archive the split manifest before final evaluation.

The discount conversation and pilot are already visible development examples. They cannot be counted as unseen final tests. The held-out set measures performance on new local tasks; pretrained benchmark contamination cannot be ruled out simply by keeping local files separate.
