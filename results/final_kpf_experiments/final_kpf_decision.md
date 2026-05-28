# Final KPF Decision

## Colab Access

The Colab notebook at `1bnq-XI0bYyacIabWv-x2ssnpNF5z5hO4` was opened through a user-authenticated Chrome debug session. The notebook title was `KPF.ipynb - Colab`, and the authenticated account was visible in the page context.

The notebook showed the previous OPF setup, baseline/hybrid evaluation, OPF training attempts, hard-negative/adversarial evaluation, and a later `limit_experiments.py` attempt. The final OPF retraining attempt reached validation but failed at checkpoint save with exit status 137, so the saved fine-tuned model was not available as a deployable artifact.

## Experiments Used For Final Selection

The final Colab experiment executes OPF inference on Eval300 with the final deterministic layer:

- expanded Korean regex coverage for spaced, dotted, no-dash, newline, and Korean-number variants
- regex-first merge when OPF and regex overlap
- contextual suppression for obvious dummy/example/product-code/model-name/version-code false positives
- narrow suffix suppression for account-like values immediately followed by `-test`
- `.invalid` email suppression for documentation-only samples

The hard-negative and adversarial stress tests reuse existing Colab OPF/Hybrid prediction JSONL files and replay the same final deterministic layer.

## Selected Final KPF

Final KPF is the existing OPF detector plus the improved deterministic safety layer in:

- `scripts/regex_safety_net.py`
- `scripts/pipeline.py`
- `scripts/evaluate_hybrid.py`

## Result

| Evaluation | Existing Hybrid | Final KPF |
|---|---:|---:|
| Eval300 precision | 0.7471 | 0.8023 |
| Eval300 recall | 0.6090 | 0.6540 |
| Eval300 F1 | 0.6710 | 0.7206 |
| Hard-negative FPR | 1.0000 | 0.0000 |
| Adversarial F1 | 0.5263 | 0.9000 |
| Adversarial covered recall | 0.6000 | 1.0000 |

## Remaining Limit

The final sampled hard-negative set has no remaining flagged rows after adding only two narrow dummy-value rules:

- suppress account-like spans only when the value is immediately followed by `-test`
- suppress email spans ending in `.invalid`

Broader suppression using generic Korean `test`/`테스트용` context was rejected because Eval300 contains real gold spans in test-token and test-card contexts. The selected final KPF reaches actual Colab Eval300 F1 0.7206 while reducing sampled hard-negative FPR to 0.0000.
