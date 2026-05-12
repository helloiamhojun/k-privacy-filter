# Extra Evaluation Summary

## Hybrid extra evaluation

| System | Korean F1 | Critical Recall | Hard Negative FPR | Adversarial Exact Recall | Adversarial Covered Recall |
|---|---:|---:|---:|---:|---:|
| Hybrid | 0.6710 | 0.8129 | 1.0000 | 0.5000 | 0.6000 |

## Interpretation

The Hybrid pipeline improved Korean PII detection on the original 300-example evaluation set, but the extra evaluation shows two important limitations.

1. Hard Negative FPR is 1.0000.
   - On PII-looking non-PII examples, the system predicts at least one span for every sentence.
   - This means the current Regex Safety Net is highly recall-oriented and over-masks PII-shaped dummy values such as order numbers, sample API keys, and test identifiers.

2. Adversarial Exact Recall is 0.5000.
   - The system exactly detects 5 out of 10 adversarial PII spans.
   - It misses or boundary-mismatches transformed formats such as spaced identifiers, Korean-number phone strings, or obfuscated emails.

3. Adversarial Covered Recall is 0.6000.
   - The system covers 6 out of 10 adversarial gold spans.
   - Covered recall is higher than exact recall, which means some failures are boundary precision issues rather than complete misses.

## Slide wording

The hybrid system is strong for standard Korean PII patterns, but it is conservative: it prefers masking suspicious PII-shaped strings over preserving all benign identifiers. This is acceptable for a privacy-first filter, but future work should add context-aware false-positive reduction.

## One-line takeaway

Hybrid improves normal Korean PII detection, but hard negatives reveal the recall-first tradeoff of deterministic regex safety nets.
