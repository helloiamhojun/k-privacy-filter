# Final KPF Offline Experiments

Existing OPF/Hybrid predictions were reused, then the final regex expansion and contextual false-positive suppression were applied.

## Main Eval 300

| System | Precision | Recall | F1 | Covered Recall | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| existing_hybrid | 0.7471 | 0.6090 | 0.6710 | 0.7796 | 87 | 165 |
| final_kpf | 0.7703 | 0.6280 | 0.6919 | 0.7796 | 79 | 157 |

## Sampled Hard Negative 100

| System | Flagged | FPR |
|---|---:|---:|
| existing_hybrid | 100/100 | 1.0000 |
| final_kpf | 0/100 | 0.0000 |

This FPR is measured only on the fixed 100-row hard-negative set whose gold spans are empty. It is a sampled stress-test result, not a universal false-positive-rate estimate.

## Adversarial 10

| System | Precision | Recall | F1 | Covered Recall | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| existing_hybrid | 0.5556 | 0.5000 | 0.5263 | 0.6000 | 4 | 5 |
| final_kpf | 0.9000 | 0.9000 | 0.9000 | 1.0000 | 1 | 1 |

## Remaining Hard-Negative False Positives

- None in the sampled hard-negative set.
