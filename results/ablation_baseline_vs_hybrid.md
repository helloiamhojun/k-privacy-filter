# Baseline vs Hybrid Ablation

| run_name                    |   seqeval_precision |   seqeval_recall |   seqeval_f1 |   critical_recall |   false_positive_rate |   seconds_per_example |
|:----------------------------|--------------------:|-----------------:|-------------:|------------------:|----------------------:|----------------------:|
| baseline_opf_eval300        |              0.6716 |           0.5332 |       0.5945 |            0.7626 |                0.3284 |                0.9992 |
| hybrid_opf_regex_eval300    |              0.7471 |           0.6090 |       0.6710 |            0.8129 |                0.2529 |                0.9834 |
| delta_hybrid_minus_baseline |              0.0755 |           0.0758 |       0.0766 |            0.0504 |               -0.0755 |               -0.0158 |
