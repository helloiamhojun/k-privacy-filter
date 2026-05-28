# K-Privacy Filter 최종 시연 영상 가이드

## 추천 길이
2분 30초에서 3분 30초가 가장 좋습니다.
핵심은 "Colab에서 실제 실행된다", "Gradio에서 마스킹된다", "hard-negative 0은 고정 샘플 기준이다"를 분명히 보여주는 것입니다.

## 녹화 도구
가장 안정적인 방법은 OBS Studio입니다.
간단히 녹화하려면 Chrome 또는 PowerPoint 창을 클릭한 뒤 `Win + G`로 Windows 녹화를 켜도 됩니다.

## 녹화 전 준비
Colab에서 아래를 실행합니다.

```bash
%cd /content/drive/MyDrive/k-privacy-filter
!python scripts/demo.py
```

Gradio public URL이 나오면 새 탭에서 엽니다.
시연은 fine-tuned 단독 모델이 아니라 최종 hybrid KPF 경로로 진행한다고 말합니다.

## 영상 구성

### 0:00-0:20 표지
말하기:

> 안녕하세요. K-Privacy Filter 최종 시연입니다. 이 시스템은 OpenAI Privacy Filter에 한국형 Regex Safety Net과 문맥 기반 오탐 억제를 결합해 한국어 개인정보를 마스킹합니다.

### 0:20-0:50 Colab 실행 확인
보여줄 것:

```bash
%cd /content/drive/MyDrive/k-privacy-filter
!ls scripts
!ls results/final_presentation
```

말하기:

> 지금 실행 위치는 Google Drive 안의 프로젝트 폴더입니다. 코드, 평가 결과, 발표 자료가 모두 저장되어 있습니다.

### 0:50-1:40 정상 마스킹
입력:

```text
주소는 경기도 화성시 동탄역로 150 102동 3804호야. 그리고 내 이름은 최호준이고, api 키는 sk-129slkdjflksjflkdjf83slkdjflskj4e398i야.
```

말하기:

> 주소, 이름, secret이 각각 placeholder로 바뀌는지 확인합니다. 핵심은 한국어 주소와 코드형 secret을 같이 처리한다는 점입니다.

### 1:40-2:15 아이디와 비밀번호
입력:

```text
아이디는 chjspd고, 비밀번호는 chIghwns1011!@!이야.
```

말하기:

> 비밀번호는 secret으로 마스킹되어야 합니다. 아이디는 프로젝트 정책에 따라 계정 식별자로 처리할 수 있습니다. fine-tuned 단독 모델에서는 이 부분이 흔들렸기 때문에 최종 시연은 hybrid KPF로 진행합니다.

### 2:15-2:55 Hard-negative
입력:

```text
모델명은 900101-1234567-A입니다.
```

말하기:

> 이 값은 주민번호처럼 보이지만 실제 개인정보가 아니라 모델명입니다. 최종 KPF의 hard-negative FPR 0은 이런 고정 반례 100개 안에서 0개를 잘못 잡았다는 뜻입니다. 전체 오탐률이 0이라는 뜻은 아닙니다.

### 2:55-3:20 결과 요약
말하기:

> 최종 replay 기준 Eval300 F1은 0.6919, hard-negative 100개에서는 0 FP, adversarial 10개에서는 F1 0.9000입니다. Fine-tuning은 저장까지 성공했지만 단독 평가가 불안정해서 최종 배포 후보로 쓰지 않았습니다.

## 제출 전 체크리스트
- Colab 또는 Gradio 화면이 보인다.
- 정상 마스킹 예시가 1개 이상 보인다.
- hard-negative 예시를 보여준다.
- "Hard-negative FPR 0은 고정 100개 샘플 기준"이라고 말한다.
- 실제 개인정보 대신 가짜 예시만 사용한다.
- 영상 길이가 4분을 넘지 않는다.
