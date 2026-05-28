# Fine-tuning Result Summary

## Status
초기 retraining 시도는 checkpoint 저장 단계에서 실패했지만, 이후 Colab에서 한국형 synthetic PII 데이터셋을 크게 생성해 fine-tuning 저장까지 성공했습니다.

## Successful run
- Dataset: train 50,000 / validation 5,000 / test 5,000
- Training subset: train 20,000 / validation 2,000
- Model: DistilBERT multilingual token classifier
- Saved artifact: `results/korean_pii_finetune/distilbert_mbert_20k_20260529_success/final/model.safetensors`
- Training loss: 0.039296
- Synthetic validation entity F1: 1.0000

## Standalone evaluation
- Synthetic test 5000 exact F1: 0.9912
- Eval300 exact F1: 0.6052
- Hard-negative 100 empty-row FPR: 0.5700
- Adversarial 10 exact F1: 0.2000

## Final decision
Fine-tuning 저장은 성공했지만 단독 모델은 실제 평가와 hard-negative에서 불안정했습니다.
따라서 최종 시연과 발표의 deploy candidate는 `OpenAI Privacy Filter + Korean Privacy Rule Pack + Context Filter` hybrid KPF입니다.
