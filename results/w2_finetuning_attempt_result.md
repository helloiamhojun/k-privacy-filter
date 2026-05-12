# W2 Fine-tuning Attempt Result

## Result

Official `opf train` successfully ran training and validation, but checkpoint saving failed in Colab.

Observed:
- full run: 4800 train / 1200 validation
  - train_loss: 0.269795
  - val_loss: 0.144646
  - val_token_accuracy: 0.9600
  - save result: interrupted during checkpoint saving
- subset run: 1000 train / 250 validation
  - train_loss: 0.526456
  - val_loss: 0.250901
  - val_token_accuracy: 0.9362
  - exit code: 137
  - saved files: config.json only
  - missing: model.safetensors

## Decision

Proceed with baseline `openai/privacy-filter` plus Korean Regex Safety Net for the working demo.

This keeps the project deliverable safe:
- working model inference
- Korean PII coverage
- measurable baseline vs hybrid comparison
- Gradio demo
