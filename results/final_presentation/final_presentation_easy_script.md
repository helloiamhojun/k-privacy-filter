# K-Privacy Filter 쉬운 설명 대본

## 한 문장 요약
이 프로젝트는 한국어 문장 속 개인정보를 찾아서 `<SECRET>`이나 `<PRIVATE_PERSON>`처럼 가려 주는 필터입니다.

## 발표에서 꼭 기억할 말
- 최종본은 fine-tuning 모델 하나가 아니라 hybrid KPF입니다.
- hybrid KPF는 OPF, 한국형 정규식, 문맥 오탐 제거를 합친 방식입니다.
- Hard-negative FPR 0은 고정 샘플 100개에서만 0이라는 뜻입니다.
- Fine-tuning은 저장 성공했지만, 실제 평가에서 오탐이 많아서 최종 시연에는 쓰지 않았습니다.

## 숫자 쉽게 읽기
- Precision: 잡았다고 한 것 중 진짜 개인정보 비율입니다. 높으면 헛잡기가 적습니다.
- Recall: 실제 개인정보 중 얼마나 잡았는지입니다. 높으면 놓치는 게 적습니다.
- F1: Precision과 Recall을 같이 보는 균형 점수입니다.
- FPR: 개인정보가 아닌데 잘못 잡은 비율입니다. 낮을수록 좋습니다.
- Hard-negative: 개인정보처럼 생겼지만 실제 개인정보가 아닌 반례입니다.
- Adversarial: 일부러 필터를 속이려고 만든 어려운 입력입니다.

## 발표 흐름
1. 한국어 개인정보는 주소, 주민번호, 계좌, secret처럼 형태가 다양하다고 말합니다.
2. OPF만 쓰면 한국형 패턴을 놓치거나 예시값을 과하게 잡을 수 있다고 말합니다.
3. 그래서 OPF + Regex Safety Net + Context Filter를 결합했다고 말합니다.
4. Eval300 F1은 0.7294, adversarial F1은 0.9000이라고 말합니다.
5. Hard-negative 100개에서는 0개를 잘못 잡았지만, 전체 오탐률 0은 아니라고 꼭 덧붙입니다.
6. Fine-tuning은 `model.safetensors` 저장까지 성공했지만 hard-negative 오탐이 높아서 최종본에서 제외했다고 말합니다.
7. 시연은 Colab에서 `python scripts/demo.py`를 실행하고 Gradio 화면으로 보여줍니다.

## 질문이 들어왔을 때
Q. Hard-negative FPR이 0이면 완벽한 건가요?
A. 아닙니다. 정해진 hard-negative 100개 샘플에서는 오탐이 없었다는 뜻입니다. 그래서 저는 전체 오탐률 0이라고 말하지 않고, 반례 세트에서 이전 방식보다 좋아졌다고 설명합니다.

Q. Fine-tuning 했는데 왜 안 쓰나요?
A. 저장은 성공했지만 실제 평가에서 최종 hybrid KPF보다 낮았고, hard-negative 오탐이 높았습니다. 보안 프로젝트에서는 좋아 보이는 모델보다 안정적으로 검증된 경로를 쓰는 것이 맞다고 판단했습니다.

Q. 이 프로젝트에서 AI를 어떻게 썼나요?
A. AI에게 코드를 한 번에 만들게 한 것이 아니라, 데이터 생성, Colab 실행, 오류 분석, 평가, PPT 작성까지 계속 지시하고 검증했습니다. Git commit과 결과 파일로 과정도 남겼습니다.
