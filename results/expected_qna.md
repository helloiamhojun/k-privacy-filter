# Expected Q&A

## Q1. 왜 LoRA fine-tuning 결과 모델을 최종 데모에 쓰지 않았나요?

Official opf train으로 학습과 validation까지는 완료했습니다. Full run에서 val_loss 0.144646, val_token_accuracy 0.9600까지 확인했습니다. 하지만 Colab 환경에서 checkpoint saving 단계가 반복적으로 interruption/SIGKILL로 실패했고, model.safetensors가 저장되지 않았습니다. 4주 압축 일정에서는 저장되지 않은 모델을 계속 붙잡기보다, 재현 가능한 baseline OPF + Korean Regex Safety Net 파이프라인으로 전환했습니다.

## Q2. 그러면 이 프로젝트는 fine-tuning 프로젝트라고 볼 수 있나요?

최종 데모 기준으로는 fine-tuned checkpoint를 사용하지 못했습니다. 대신 fine-tuning 데이터 구축, opf train 포맷 변환, 학습/validation 실행까지 수행했고, 최종 산출물은 hybrid privacy filtering system으로 정리했습니다. 발표에서는 fine-tuned model deployment가 아니라 Korean PII adaptation pipeline으로 설명하는 것이 정확합니다.

## Q3. 평가셋이 template-based이면 성능이 과대평가된 것 아닌가요?

맞습니다. 평가셋은 300개 template-based Korean examples라 production benchmark는 아닙니다. 그래서 결과를 일반 한국어 전체 성능으로 주장하지 않고, 주민번호/사업자번호/API key/전화번호 같은 controlled Korean PII 패턴에서 hybrid safety net이 baseline보다 개선되는지 확인한 실험으로 해석했습니다.

## Q4. Regex를 쓰면 ML 프로젝트 의미가 약해지지 않나요?

이 프로젝트의 목표는 privacy filtering system입니다. 정형 PII는 regex가 더 안정적인 경우가 많고, 비정형 PII는 OPF가 담당합니다. 따라서 ML model과 deterministic safety net을 결합하는 hybrid design이 실제 보안 시스템에 더 적합합니다.

## Q5. False positive는 어떻게 다뤘나요?

OPF가 한국어에서 span boundary를 넓게 잡는 사례가 있었습니다. 예를 들어 주소 뒤의 종결 표현까지 포함하는 경우가 있어 pipeline 후처리에서 address span boundary trim을 적용했습니다. 평가에서는 false_positive_rate를 따로 측정했고, hybrid 방식은 baseline 0.3284에서 0.2529로 낮아졌습니다.
