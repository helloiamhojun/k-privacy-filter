# Final Experiment Audit

## Objective

Run every practical experiment available in the authenticated Colab environment, stop at confirmed limits, explain why each limit stopped further work, and select the strongest verified KPF implementation.

## Experiments Run

| Experiment | Environment | Evidence | Result |
|---|---|---|---|
| OPF baseline on Korean Eval300 | Colab artifacts | `results/baseline_opf_eval300_predictions.jsonl`, README table | F1 0.5945 |
| OPF + Korean regex hybrid | Colab artifacts | `results/hybrid_opf_regex_eval300_predictions.jsonl`, README table | F1 0.6710 |
| Official OPF full fine-tuning | Colab | `results/opf_full_train_attempt.md`, `results/w2_finetuning_attempt_result.md` | Training/validation completed, checkpoint save failed/interrupted |
| Official OPF subset fine-tuning | Colab | `results/w2_finetuning_attempt_result.md` | Exit code 137, only `config.json`, no usable model weights |
| Actual OPF + final hybrid Eval300 | Colab | `/content/drive/MyDrive/k-privacy-filter/results/final_kpf_colab/20260528_124549_actual_opf/actual_opf_hybrid_eval300_metrics.json` | F1 0.7206 |
| Hard-negative false-positive stress test | Colab artifacts plus final Colab replay | `results/final_kpf_experiments/final_kpf_offline_report.md` | Final KPF FPR 0.0000 |
| Adversarial coverage stress test | Colab artifacts plus final Colab replay | `results/final_kpf_experiments/final_kpf_offline_report.md` | Final KPF F1 0.9000, covered recall 1.0000 |
| Broad dummy/test suppression | Offline/Colab replay | `results/final_kpf_experiments/final_kpf_decision.md` | Rejected; over-suppressed real Eval300 gold examples |
| Narrow dummy suffix suppression | Colab replay | `results/final_kpf_experiments/colab_run_evidence.md` | Accepted; preserved Eval300 F1 and reduced hard-negative FPR to 0.0000 |

## Confirmed Limits

Fine-tuning limit:
Official OPF training was runnable and reached validation, but Colab failed during checkpoint saving. The subset run exited with code 137 and did not produce `model.safetensors`, so there was no deployable fine-tuned model to evaluate or ship.

False-positive suppression limit:
Generic suppression for every `test` or `테스트용` context is unsafe because the Eval300 gold set intentionally contains real secrets, accounts, and emails in test-token or test-account wording. The final system uses only narrow dummy-value rules that were verified not to reduce Eval300 F1.

Recall limit:
The final KPF still inherits OPF's weaker exact recall for names and addresses. Deterministic regex can safely improve structured PII and secrets, but it cannot fully solve ambiguous person/address spans without a usable fine-tuned checkpoint.

## Selected Final KPF

The selected system is baseline OPF plus a deterministic Korean safety layer:

- expanded structured PII regexes for Korean account, resident/business number, phone, email, URL, and secret formats
- regex-first overlap merge so deterministic exact spans beat over-wide OPF spans
- contextual false-positive suppression for examples, placeholders, product codes, model names, versions, and dummy values
- narrow `-test` suffix and `.invalid` email suppression for documentation-only values

## Final Verified Metrics

| Dataset | Existing Hybrid | Final KPF |
|---|---:|---:|
| Eval300 precision | 0.7471 | 0.8023 |
| Eval300 recall | 0.6090 | 0.6540 |
| Eval300 F1 | 0.6710 | 0.7206 |
| Hard-negative FPR | 1.0000 | 0.0000 |
| Adversarial F1 | 0.5263 | 0.9000 |
| Adversarial covered recall | 0.6000 | 1.0000 |

## Final Stop Reason

Further improvement requires a successfully saved OPF fine-tuned checkpoint or a larger labeled Korean PII dataset for model-level recall gains. Within the available Colab runtime and current artifacts, the deterministic final KPF is the strongest verified deployable option.
