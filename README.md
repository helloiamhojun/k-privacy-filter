# K-Privacy Filter

K-Privacy Filter is a Korean privacy filtering demo based on OpenAI Privacy Filter plus a deterministic Korean Regex Safety Net.

## Pipeline

1. OpenAI Privacy Filter detects general PII spans.
2. Korean Regex Safety Net detects deterministic Korean PII patterns.
3. Overlapping spans are merged, with regex exact spans preferred on overlap.
4. Contextual dummy/example false positives are suppressed.
5. Detected spans are replaced with typed placeholders.

## Labels

- private_person
- private_address
- private_email
- private_phone
- private_url
- private_date
- account_number
- secret

Korean resident registration numbers and business registration numbers are mapped to `account_number`.

## Dataset

- Korean evaluation set: 300 template-based examples
- Synthetic training set: 5,000 Faker-based Korean examples
- KLUE-NER auxiliary set: 1,000 mapped examples for person/location spans

## Results

Main evaluation set: 300 Korean examples.

| System / Set | Precision | Recall | Exact F1 | Covered Recall | False Positive |
|---|---:|---:|---:|---:|---:|
| Baseline OPF / Eval300 | 0.6716 | 0.5332 | 0.5945 | - | 0.3284 FPR |
| Existing hybrid / Eval300 | 0.7471 | 0.6090 | 0.6710 | 0.7796 | 87 FP |
| Final KPF / Eval300 | 0.7703 | 0.6280 | 0.6919 | 0.7796 | 79 FP |

Final KPF executes OPF inference plus the final deterministic layer:
expanded Korean regex coverage, regex-first span merge, contextual false-positive suppression, and targeted dummy-value suppression.

Additional sampled stress tests:

| Test | Previous Hybrid | Final KPF |
|---|---:|---:|
| Sampled hard-negative 100 flagged | 100 / 100 | 0 / 100 |
| Adversarial exact F1 | 0.5263 | 0.9000 |
| Adversarial covered recall | 0.6000 | 1.0000 |

The hard-negative result is measured only on the fixed 100-row sampled stress set. It is not a claim that the universal false-positive rate is zero.

## Fine-Tuning Note

The project also generated a larger Korean-style synthetic PII dataset and completed a saveable fine-tuning run in Colab.

- Dataset: train 50,000 / validation 5,000 / test 5,000
- Base model: `distilbert-base-multilingual-cased`
- Training subset: train 20,000 / validation 2,000
- Saved checkpoint: `results/korean_pii_finetune/distilbert_mbert_20k_20260529_success/final/model.safetensors`

Standalone fine-tuned evaluation:

| Dataset | Exact F1 | Empty-row FPR | Decision |
|---|---:|---:|---|
| Synthetic test 5000 | 0.9912 | 0.0000 | synthetic distribution only |
| Eval300 | 0.6052 | 0.0000 | below final KPF |
| Hard-negative 100 | 0.0000 | 0.5700 | too many false positives |
| Adversarial 10 | 0.2000 | 0.0000 | weak against tricky inputs |

Final decision: the fine-tuned checkpoint is useful experimental evidence, but the final demo and presentation use the hybrid OPF + Korean Regex Safety Net + Context Filter pipeline.

Earlier `opf train` attempts:

- 4,800 train / 1,200 validation:
  - train_loss: 0.269795
  - val_loss: 0.144646
  - val_token_accuracy: 0.9600
  - checkpoint save failed
- 1,000 train / 250 validation:
  - train_loss: 0.526456
  - val_loss: 0.250901
  - val_token_accuracy: 0.9362
  - checkpoint save failed with exit code 137

The final demo uses the stable hybrid pipeline: baseline OpenAI Privacy Filter plus deterministic Korean regex backup and contextual false-positive suppression.

## Demo

Run:

    python scripts/demo.py

Example input:

    이름은 김민수입니다. 주민번호는 900101-1234567이고 전화는 010-1234-5678입니다.

Example output:

    이름은 <PRIVATE_PERSON>입니다. 주민번호는 <ACCOUNT_NUMBER>이고 전화는 <PRIVATE_PHONE>입니다.

## Main Files

- scripts/pipeline.py
- scripts/regex_safety_net.py
- scripts/evaluate_final_kpf_offline.py
- scripts/demo.py
- scripts/evaluate_hybrid.py
- data/raw/korean_eval_300.jsonl
- data/processed/synthetic_train_5000.jsonl
- results/ablation_baseline_vs_hybrid.md
- results/final_kpf_experiments/final_experiment_audit.md
- results/final_kpf_experiments/colab_run_evidence.md
- results/final_presentation/K-Privacy-Filter-final-presentation.pptx
- results/final_presentation/final_presentation_script.md
- results/final_presentation/final_presentation_easy_script.md
- results/final_presentation/final_presentation_glossary.md

## License

OpenAI Privacy Filter: Apache 2.0.
KLUE: CC-BY-SA-4.0.
