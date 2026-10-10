# Revity synthetic starter datasets

Version 0.1.0 contains **12,000 generated examples across six task families**:
integer arithmetic, linear equations, sorting, unit conversion, word counting,
and Boolean comparisons. Every answer is calculated by Python; no scraped
content, external training datasets, or model-generated answers are included.

Each task contributes 1,600 training, 200 validation, and 200 test examples:
9,600 training, 1,200 validation, and 1,200 test rows overall. Records use `id`,
`task`, `split`, and user/assistant `messages`. IDs are SHA-256 hashes of prompts.
A global uniqueness check prevents identical prompts across splits. The manifest
records generation seed, row counts, task counts, and file checksums.

## Reproduce

Requires Python 3.10+ and only the standard library. From the repository root:

```sh
python scripts/build_datasets.py --output data/generated
python -m unittest discover -s tests -v
```

The output directory must be empty. Use a new directory for another run.

## Evaluate a model

Run your model separately on the **user messages only**, then create a JSONL file
with one `{"id": "<example ID>", "prediction": "<model answer>"}` record per input.
Do not send the reference assistant answers to the model.

```sh
python scripts/evaluate.py --dataset data/generated/test.jsonl --predictions predictions.jsonl
```

The scorer rejects missing, duplicate, or extra prediction IDs and refuses the
training split. Accuracy uses exact matching after trimming leading/trailing
whitespace; equivalent alternative answer formats may score as incorrect.
Record the exact model, quantization, inference settings, hardware, dataset hash,
and inference software version alongside any published score.

## Limits and provenance

This is narrow, template-based synthetic data, **not a broad knowledge corpus**.
Splits share templates and distributions, so they measure in-distribution task
performance, not general reasoning or unseen-task generalization. Published test
answers are inspectable; these are development checks, not a secure benchmark.
No decontamination against any base model's training data has been performed.
No Qwen model was used to create this data. No model has been trained or evaluated
with this package, and no performance or environmental benefit is established.
These simple tasks cannot make a giant model capable on their own.

Generated dataset contents are dedicated under CC0 1.0:
https://creativecommons.org/publicdomain/zero/1.0/
This dedication applies to the generated data only and does not license external
models or change the licensing of the repository's source code.
