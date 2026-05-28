# Final Presentation Package

이 폴더는 K-Privacy Filter 최종 발표용 산출물입니다.

## Main files
- `K-Privacy-Filter-final-presentation-20260529.pptx`: 최신 최종 발표 PPT
- `final_presentation_script.md`: 슬라이드별 발표 대본
- `final_presentation_easy_script.md`: 발표자가 이해하기 쉽게 풀어쓴 설명
- `final_presentation_glossary.md`: 어려운 용어 설명
- `final_demo_video_guide.md`: 최종 시연 영상 촬영 가이드
- `final_result_table.md`: 최종 성능 요약 표
- `final_demo_cases.md`: 시연용 예시

## Core result

| Metric | Baseline OPF | Existing hybrid | Final KPF |
|---|---:|---:|---:|
| Eval300 Precision | 0.6716 | 0.7471 | 0.7994 |
| Eval300 Recall | 0.5332 | 0.6090 | 0.6706 |
| Eval300 Exact F1 | 0.5945 | 0.6710 | 0.7294 |
| Eval300 Covered Recall | - | 0.7796 | 0.8009 |
| Eval300 False Positive | 0.3284 FPR | 87 FP | 71 FP |
| Hard-negative 100 flagged | - | 100 / 100 | 0 / 100 |
| Adversarial 10 F1 | - | 0.5263 | 0.9000 |

Note: hard-negative FPR 0.0000은 고정 100개 hard-negative 샘플에서의 결과입니다. 전체 오탐률이 0이라는 주장이 아닙니다.

## Fine-tuning decision
한국형 synthetic PII 데이터셋 50,000 / 5,000 / 5,000을 만들고 DistilBERT multilingual token classifier를 학습했습니다.
Colab Drive에 `final/model.safetensors` 저장까지 성공했습니다.
하지만 단독 fine-tuned 모델은 Eval300 F1 0.6052, hard-negative empty-row FPR 0.5700, adversarial F1 0.2000으로 최종 hybrid KPF보다 불안정해 최종 시연에서 제외했습니다.
