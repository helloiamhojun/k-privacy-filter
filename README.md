# K-Privacy Filter

K-Privacy Filter is a Korean privacy filtering demo based on OpenAI Privacy Filter plus a deterministic Korean Regex Safety Net.

## Pipeline

1. OpenAI Privacy Filter detects general PII spans.
2. Korean Regex Safety Net detects deterministic Korean PII patterns.
3. Overlapping spans are merged.
4. Detected spans are replaced with typed placeholders.

## Labels

- private_person
- private_address
- private_email
- private_phone
- private_url
- private_date
- account_number
- secret

Korean resident registration numbers and business registration numbers are mapped to account_number.

## Dataset

- Korean evaluation set: 300 template-based examples
- Synthetic training set: 5,000 Faker-based Korean examples
- KLUE-NER auxiliary set: 1,000 mapped examples for person/location spans

## Results

Evaluation set: 300 Korean examples.

| Run | Precision | Recall | F1 | Critical Recall | FPR | Latency |
|---|---:|---:|---:|---:|---:|---:|
| OpenAI Privacy Filter baseline | 0.6716 | 0.5332 | 0.5945 | 0.7626 | 0.3284 | 0.9992s |
| OPF + Korean Regex Safety Net | 0.7471 | 0.6090 | 0.6710 | 0.8129 | 0.2529 | 0.9834s |
| Delta | +0.0755 | +0.0758 | +0.0766 | +0.0504 | -0.0755 | -0.0158s |

## Fine-tuning Note

Official opf train completed training and validation on Korean synthetic/KLUE data, but checkpoint saving repeatedly failed in Colab with interruption/SIGKILL.

Observed training attempts:

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

The final demo uses the stable hybrid pipeline: baseline OpenAI Privacy Filter plus deterministic Korean regex backup.

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
- scripts/demo.py
- scripts/evaluate_hybrid.py
- data/raw/korean_eval_300.jsonl
- data/processed/synthetic_train_5000.jsonl
- results/ablation_baseline_vs_hybrid.md

## License

OpenAI Privacy Filter: Apache 2.0.
KLUE: CC-BY-SA-4.0.
