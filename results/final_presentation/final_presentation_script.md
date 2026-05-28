# K-Privacy Filter 최종 발표 대본

## 1장. 표지
안녕하세요. K-Privacy Filter 최종 구현과 평가 결과를 발표하겠습니다.
이 프로젝트의 목표는 한국어 문장 안에 섞인 주소, 이름, 계좌, 주민번호, 비밀번호, API key 같은 민감정보를 자동으로 마스킹하는 것입니다.

최종 구현체는 OpenAI Privacy Filter만 쓰지 않고, 한국형 Regex Safety Net과 문맥 기반 오탐 억제를 결합했습니다.
최종 replay 기준 Eval300 F1은 0.6919, adversarial F1은 0.9000입니다.
Hard-negative FPR 0.0000은 고정 샘플 100개에서 0개를 잘못 잡았다는 뜻이지, 전체 세상에서 오탐이 0이라는 뜻은 아닙니다.

## 2장. 핵심 메시지
발표 평가 기준에 맞춰 네 가지로 설명하겠습니다.
첫째, Creativity는 한국어 개인정보와 생성형 AI 사용 흐름을 연결한 점입니다.
둘째, Completeness는 Colab에서 실제 실행되는 필터, Gradio 시연, 평가 파일까지 완성했다는 점입니다.
셋째, AI-Collaboration은 AI에게 코드만 맡긴 것이 아니라 실험 설계, 디버깅, 오류 분석, 발표 정리까지 계속 디렉팅했다는 점입니다.
넷째, Professionalism은 성능을 과장하지 않고 실패한 fine-tuning 결과까지 공개한다는 점입니다.

핵심 결론은 최종 배포 후보가 fine-tuned 단독 모델이 아니라, 실전 오탐을 줄인 Hybrid KPF라는 것입니다.

## 3장. 문제 정의
한국어 개인정보는 범용 필터만으로는 놓치거나 과하게 잡힐 수 있습니다.
예를 들어 "경기도 화성시 동탄역로 150 102동 3804호"처럼 주소 경계가 길고, "chIghwns1011!@!" 같은 비밀번호나 "sk-"로 시작하는 API key도 문장 안에 섞입니다.

반대로 모델명, 주문번호, 예시값처럼 개인정보처럼 보이지만 실제 개인정보가 아닌 값도 있습니다.
그래서 목표는 두 가지입니다. 진짜 민감정보는 놓치지 않고, 개인정보가 아닌 값은 가능한 한 덜 지우는 것입니다.

## 4장. 최종 시스템 아키텍처
최종 KPF는 다섯 단계입니다.
첫째, 사용자가 입력한 텍스트가 들어옵니다.
둘째, OPF가 범용 개인정보 후보 span을 찾습니다.
셋째, Regex Safety Net이 한국형 주민번호, 주소, 전화번호, 계좌, secret 패턴을 보강합니다.
넷째, Context Filter가 예시, 모델명, 주문번호 같은 오탐 문맥을 제거합니다.
다섯째, 겹치는 span을 병합하고 `<PRIVATE_PERSON>`, `<SECRET>` 같은 placeholder로 바꿉니다.

구현 파일은 `scripts/pipeline.py`, `scripts/regex_safety_net.py`, `scripts/demo.py`, `scripts/evaluate_final_kpf_offline.py`입니다.

## 5장. 핵심 알고리즘
정규식은 단순한 보조가 아니라 모델의 실패 영역을 맡는 안전망입니다.
탐지 보강은 주민번호, 전화번호, 계좌, 카드, 주소, API key 등을 담당합니다.
문맥 억제는 예시, 샘플, 더미, 상품코드, 모델명, placeholder 같은 오탐을 줄입니다.
병합 정책은 regex span을 우선하고, 겹치는 결과를 합친 뒤 평가 가능한 형태로 마스킹합니다.

중요한 원칙은 "무조건 많이 지우기"가 아닙니다.
민감정보는 잡되, 실제 개인정보가 아닌 코드나 예시는 가능한 한 제거해야 실사용성이 생깁니다.

## 6장. 구현체와 산출물
실행 경로는 Google Colab과 Drive입니다.
Colab에서 Drive를 mount하고 `/content/drive/MyDrive/k-privacy-filter`로 이동한 뒤 `python scripts/demo.py`를 실행합니다.
그러면 Gradio public URL이 생성되고, 그 화면에서 직접 입력과 마스킹 결과를 확인할 수 있습니다.

평가 결과는 `results/final_kpf_experiments/`에 있고, fine-tuning 결과와 checkpoint는 `results/korean_pii_finetune/`에 있습니다.
PPT, 대본, 시연 가이드는 `results/final_presentation/`에 저장했습니다.

## 7장. 평가 결과
Eval300에서 baseline OPF의 F1은 0.5945였습니다.
기존 hybrid는 0.6710이었고, 최종 KPF는 0.6919까지 올라갔습니다.
Precision은 0.7703, Recall은 0.6280이고, false positive는 79개입니다.

Hard-negative 100개에서는 최종 KPF가 0개를 flag했습니다.
이 말은 "정해진 반례 100개 안에서는 오탐이 없었다"는 뜻입니다.
전체 데이터에서 오탐률이 영원히 0이라는 의미가 아니므로, 발표에서 반드시 샘플 기준이라고 말해야 합니다.

Adversarial 10개에서는 F1 0.9000이 나왔습니다.
즉 일반 평가, 반례 평가, 우회형 평가를 함께 보면서 최종 모델을 판단했습니다.

## 8장. Fine-tuning 실험
한국형 synthetic PII 데이터셋을 크게 만들고 fine-tuning도 수행했습니다.
데이터는 train 50,000, validation 5,000, test 5,000이고, DistilBERT multilingual token classifier를 학습했습니다.
Colab Drive에 `final/model.safetensors` 저장까지 성공했습니다.

하지만 단독 fine-tuned 모델은 최종 배포 후보로 쓰지 않았습니다.
Synthetic test에서는 F1 0.9912로 좋아 보였지만, Eval300에서는 F1 0.6052로 최종 KPF보다 낮았습니다.
Hard-negative 100에서는 empty-row FPR이 0.5700으로 높았고, adversarial 10에서는 F1 0.2000이었습니다.

그래서 이 결과는 연구 트랙으로 보관하고, 최종 시연은 hybrid KPF로 진행합니다.

## 9장. Live Demonstration
시연은 Colab에서 `python scripts/demo.py`를 실행하고 Gradio 화면을 띄우는 방식입니다.
첫 번째 입력은 주소, 이름, API key가 섞인 문장입니다.
기대 결과는 주소, 이름, secret이 각각 placeholder로 마스킹되는 것입니다.

두 번째 입력은 아이디와 비밀번호입니다.
비밀번호는 secret으로 마스킹하고, 아이디는 정책에 따라 계정 식별자로 처리합니다.

세 번째 입력은 hard-negative입니다.
"모델명은 900101-1234567-A입니다"는 실제 주민번호가 아니라 모델명 문맥이므로 최종 KPF에서는 마스킹하지 않는 것이 목표입니다.

## 10장. AI 및 Git 협업 성과
AI를 단순 코드 생성기로 쓰지 않고 실험 매니저처럼 디렉팅했습니다.
문제 정의, Colab 실행, 데이터 생성, 학습, 평가, 오류 분석, 발표 자료 작성까지 단계별로 지시했습니다.

정량적으로는 Git commit 9개, synthetic dataset 50k/5k/5k, 평가 세트 300/100/10, fine-tune checkpoint 저장, 최종 report 파일이 남았습니다.
중요한 점은 실패 결과도 버리지 않고 기록했다는 것입니다.
이 덕분에 질의응답에서 "왜 fine-tuning을 최종에 안 썼는가"를 근거 있게 설명할 수 있습니다.

## 11장. 한계점 및 향후 과제
현재 한계는 synthetic 데이터와 실제 사용자 데이터 사이의 차이입니다.
또 fine-tuned 단독 모델은 label confusion과 hard-negative 오탐이 있었습니다.
Adversarial set도 10개라서 모든 우회 공격을 대표하지는 못합니다.

향후 과제는 실제 문서와 로그 스타일을 반영한 데이터셋 확장, hard-negative 평가 게이트 자동화, LLM 또는 분류기 기반 context verifier 추가입니다.
보안 관점의 인사이트는 개인정보 필터가 과소탐과 과대탐을 동시에 관리해야 한다는 것입니다.

## 12장. 마무리
K-Privacy Filter는 OPF의 범용 탐지력, 한국형 Regex Safety Net, 문맥 오탐 억제를 결합한 데모 가능한 hybrid defense입니다.
최종 수치는 Eval300 F1 0.6919, hard-negative 100개 기준 0 FP, adversarial F1 0.9000입니다.

Fine-tuning은 저장까지 성공했지만 현재는 연구 트랙으로 분리했습니다.
최종 산출물은 완벽한 모델이라고 주장하기보다, 검증 가능한 방어 체계라는 점을 강조하겠습니다.
감사합니다.
