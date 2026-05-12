# Presentation Notes

## 1. Problem

OpenAI Privacy Filter performs well on general PII, but Korean deployment needs extra coverage for deterministic local identifiers such as resident registration numbers, business registration numbers, Korean phone numbers, and API keys in Korean logs.

## 2. Method

K-Privacy Filter uses a three-stage hybrid pipeline.

1. OpenAI Privacy Filter detects general PII.
2. Korean adaptation data was built from 5,000 synthetic Faker examples and 1,000 KLUE-NER mapped examples.
3. A Korean Regex Safety Net catches deterministic Korean PII patterns and merges them with OPF spans.

Final demo pipeline:
OpenAI Privacy Filter + Korean Regex Safety Net.

## 3. Results

On a 300-example Korean evaluation set:

- Baseline OPF F1: 0.5945
- Hybrid F1: 0.6710
- F1 improvement: +7.66 points
- Critical Recall: 0.7626 -> 0.8129
- False Positive Rate: 0.3284 -> 0.2529
- Latency: about 1.0 second per example on Colab T4

## 4. Fine-tuning Attempt

Official opf train successfully completed training and validation.

Best full-run validation result:
- train_loss: 0.269795
- val_loss: 0.144646
- val_token_accuracy: 0.9600

However, checkpoint saving repeatedly failed in Colab with interruption/SIGKILL. For the 4-week compressed schedule, the final deliverable was switched to the stable hybrid pipeline.

## 5. Demo Talking Point

The demo shows that deterministic Korean PII such as resident registration numbers, business registration numbers, phone numbers, and API keys are reliably caught by the regex safety net even when the baseline model misses or over-extends spans.

## 6. Limitation

The evaluation set is template-based, so the result should be interpreted as a controlled Korean PII adaptation experiment rather than a production benchmark.

## 7. Conclusion

The hybrid pipeline improved Korean PII detection while keeping latency almost unchanged. The project delivered a working privacy filter demo, evaluation table, dataset pipeline, and reproducible code within the 4-week compressed schedule.
