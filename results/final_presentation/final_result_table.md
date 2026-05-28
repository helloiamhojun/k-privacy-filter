# Final KPF Result Table

| System / Set | Precision | Recall | Exact F1 | Covered Recall | False Positive |
|---|---:|---:|---:|---:|---:|
| Baseline OPF / Eval300 | 0.6716 | 0.5332 | 0.5945 | - | 0.3284 FPR |
| Existing hybrid / Eval300 | 0.7471 | 0.6090 | 0.6710 | 0.7796 | 87 FP |
| Final KPF / Eval300 | 0.7703 | 0.6280 | 0.6919 | 0.7796 | 79 FP |

| Stress set | Existing hybrid | Final KPF | Interpretation |
|---|---:|---:|---|
| Sampled hard-negative 100 | 100 / 100 flagged | 0 / 100 flagged | 고정 반례 100개 기준 오탐 제거 |
| Adversarial 10 Exact F1 | 0.5263 | 0.9000 | 우회형 입력 성능 개선 |

Hard-negative FPR 0.0000은 고정된 100개 샘플에서만 의미합니다. 전체 환경에서 오탐률이 0이라는 뜻은 아닙니다.
