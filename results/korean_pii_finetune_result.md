# Korean PII Fine-tuning Result

## What was tested

This experiment checked whether a larger Korean-style synthetic PII dataset can be generated and used for a saveable token-classification fine-tuning run in Colab.

## Dataset

- Location in Colab Drive: `/content/drive/MyDrive/k-privacy-filter/data/processed/korean_pii_large`
- Train rows: 50,000
- Validation rows: 5,000
- Test rows: 5,000
- Hard-negative ratio: about 18%
- Labels:
  - `private_person`
  - `private_address`
  - `private_email`
  - `private_phone`
  - `private_url`
  - `private_date`
  - `account_number`
  - `secret`

The generated train split includes 8,949 empty-span hard-negative rows. Span validation passed for train, validation, and test files.

## Fine-tuning

- Environment: Google Colab
- GPU: Tesla T4
- Base model: `distilbert-base-multilingual-cased`
- Training rows used: 20,000
- Validation rows used: 2,000
- Epochs: 1
- Output directory:
  `/content/drive/MyDrive/k-privacy-filter/results/korean_pii_finetune/distilbert_mbert_20k_20260529_success`
- Final model directory:
  `/content/drive/MyDrive/k-privacy-filter/results/korean_pii_finetune/distilbert_mbert_20k_20260529_success/final`
- Saved weight file: `model.safetensors`

## Result

- Train runtime: 180.9 seconds
- Train loss: 0.039296
- Eval loss: 0.000428
- Eval token accuracy: 1.0000
- Eval entity precision: 1.0000
- Eval entity recall: 1.0000
- Eval entity F1: 1.0000
- Save check: `model.safetensors` exists

## Important caveat

These high validation numbers are from the synthetic dataset distribution, not a real-world benchmark. The result proves that the Korean dataset + fine-tuning + model saving path works in Colab. It should not be presented as proof that the model is perfect on real Korean user text.

For the final demo, the deployed K-Privacy Filter should still use the hybrid OPF + Korean Regex Safety Net unless this new checkpoint is integrated and re-evaluated on the project evaluation sets.

## Follow-up Evaluation

The saved checkpoint was loaded again and evaluated as a standalone detector.

- Evaluation output in Colab Drive:
  `/content/drive/MyDrive/k-privacy-filter/results/korean_pii_finetune/eval_20260529`
- Report file:
  `/content/drive/MyDrive/k-privacy-filter/results/korean_pii_finetune/eval_20260529/finetuned_eval_report.md`

| Dataset | Rows | Exact P | Exact R | Exact F1 | Covered R | Overlap R | Empty-row FPR | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| synthetic_test | 5,000 | 0.9912 | 0.9912 | 0.9912 | 0.9999 | 1.0000 | 0.0000 | 97 | 97 |
| eval300 | 300 | 0.6038 | 0.6066 | 0.6052 | 0.6327 | 0.8104 | 0.0000 | 168 | 166 |
| hard_negative | 100 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.5700 | 57 | 0 |
| adversarial | 10 | 0.1500 | 0.3000 | 0.2000 | 0.3000 | 0.7000 | 0.0000 | 17 | 7 |

## Error Analysis

Observed failure patterns:

- The model often classifies phone numbers such as `010-4444-5555` as `account_number` instead of `private_phone`.
- It over-detects hard-negative examples like model names, order numbers, placeholder strings, and demo values.
- It sometimes trims Korean names incorrectly, for example predicting `태형` instead of `김태형`.
- It sometimes over-expands bank-account spans by including the bank name, for example `국민 123-45-67890` instead of `123-45-67890`.
- It splits secrets into multiple fragments, especially API keys and Slack-style tokens.
- Obfuscated cases such as spaced Korean names, `[at]` emails, and spaced addresses need more targeted training data.

## Updated Decision

The fine-tuned checkpoint is useful evidence that the training-and-save pipeline works, but it should not replace the current final demo system yet.

Current best decision:

- Use the hybrid OPF + Korean Regex Safety Net for the final demo and presentation.
- Present the fine-tuned checkpoint as an additional experiment.
- Say clearly that the synthetic-test score is high, but real/hard-negative evaluation shows the model needs more negative examples, label balancing, and post-processing before deployment.
