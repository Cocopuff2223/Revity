# Revity 1.0 model target and release status

The intended upstream candidate is **Qwen/Qwen3-Coder-480B-A35B-Instruct**,
listed in [Qwen's official repository](https://github.com/QwenLM/Qwen3-Coder).
Its [official model page](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct)
is the source for weights, model-specific licensing, and inference requirements.
This identifies a candidate; it is not a claim of completed integration.

## What exists

- A generator for 12,000 synthetic starter examples across six task families.
- Disjoint prompts across training, validation, and test splits.
- An exact-match scorer and six passing automated software/data tests.
- A locally packaged dataset preview, version 0.1.0.

## What is still required

- Review the exact weight artifact's license and pin its revision and checksums.
- Obtain suitable infrastructure and the model weights. A rough 480-billion-
  parameter 4-bit weight estimate alone is 240 GB in decimal units, excluding
  quantization metadata, context cache, and other runtime memory. Training has
  additional requirements. The current cloud workspace has no GPU, 32 GiB RAM,
  and approximately 30 GB available disk; it cannot host this model.
- Choose a supported training/inference stack, prepare appropriate training data,
  and actually run training or adaptation if releasing a modified model.
- Run and record model evaluations with exact model and dataset versions.
- Package actual resulting artifacts with upstream attribution and license terms.
- Restore GitHub API access before publishing release assets. Git pushes work,
  but the repository API request returned Forbidden during preparation.

GitHub hosts downloadable artifacts; publishing a repository or release does not
train a model or provide its inference infrastructure. No Qwen weights have been
downloaded or modified, and no Revity model performance results exist yet.
The dataset preview must not be labeled as trained Revity 1.0 model weights.
