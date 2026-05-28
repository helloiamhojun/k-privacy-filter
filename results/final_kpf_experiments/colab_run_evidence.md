# Colab Run Evidence

Executed in the logged-in Google Colab runtime on 2026-05-28.

- Notebook account observed by Colab frontend: `chjspd@gmail.com`
- Runtime working directory: `/content`
- Project directory: `/content/drive/MyDrive/k-privacy-filter`
- Python: `3.12.13`
- Platform: `Linux-6.6.122+-x86_64-with-glibc2.35`
- Final run directory: `/content/drive/MyDrive/k-privacy-filter/results/final_kpf_colab/20260528_123950_ascii`
- Actual OPF Eval300 run directory: `/content/drive/MyDrive/k-privacy-filter/results/final_kpf_colab/20260528_124549_actual_opf`
- Compile command: `/usr/bin/python3 -m compileall scripts/regex_safety_net.py scripts/pipeline.py scripts/evaluate_hybrid.py scripts/evaluate_final_kpf_offline.py`
- Evaluation command: `/usr/bin/python3 scripts/evaluate_final_kpf_offline.py`
- Both commands returned `0`.

## Colab Metrics

Actual OPF + Final KPF Eval300 run:

| System | Precision | Recall | F1 | Critical Recall | FPR | Seconds/Example |
|---|---:|---:|---:|---:|---:|---:|
| baseline | 0.6716 | 0.5332 | 0.5945 | 0.7626 | 0.3284 | 1.0386 |
| final_kpf | 0.8023 | 0.6540 | 0.7206 | 0.8993 | 0.1977 | 0.9850 |

Replay/stress metrics:

| Dataset | System | Precision | Recall | F1 | Covered Recall | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|
| Main Eval 300 | existing_hybrid | 0.7471 | 0.6090 | 0.6710 | 0.7796 | 87 | 165 |
| Main Eval 300 | final_kpf | 0.7994 | 0.6706 | 0.7294 | 0.8009 | 71 | 139 |
| Adversarial 10 | existing_hybrid | 0.5556 | 0.5000 | 0.5263 | 0.6000 | 4 | 5 |
| Adversarial 10 | final_kpf | 0.9000 | 0.9000 | 0.9000 | 1.0000 | 1 | 1 |

| Dataset | System | Flagged | FPR |
|---|---|---:|---:|
| Hard Negative 100 | existing_hybrid | 100/100 | 1.0000 |
| Hard Negative 100 | final_kpf | 0/100 | 0.0000 |

Remaining hard-negative false positives:

- None in the sampled hard-negative set.
