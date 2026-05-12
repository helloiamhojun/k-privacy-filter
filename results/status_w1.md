# K-Privacy Filter Status

- mode: 4-week compressed safe mode
- current_week: W1 completed
- eval_set: 300 Korean template-based examples
- synthetic_train_set: 5,000 examples
- train_split: 4,000 synthetic examples
- val_split: 1,000 synthetic examples

## Baseline

- model: openai/privacy-filter
- device: cuda
- seqeval_precision: 0.6716
- seqeval_recall: 0.5332
- seqeval_f1: 0.5945
- exact_precision: 0.6716
- exact_recall: 0.5332
- exact_f1: 0.5945
- latency_seconds_per_example: 1.0363

## Next

W2 starts with KLUE-NER loading and mapping person/location entities.
