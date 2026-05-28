import { bg, title, footer, C, card, label, bullet, smallText, table } from "./common.mjs";

export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "AI 및 Git 협업 성과", "AI를 코드 생성기가 아니라 실험 매니저처럼 디렉팅했습니다", "실패한 실험까지 Git과 결과 파일로 남겨, 발표자가 개발 과정을 설명할 수 있게 만들었습니다.");

  card(slide, ctx, 70, 214, 500, 352, "#FFFFFF");
  label(slide, ctx, "AI 디렉팅 방식", 96, 238, 130, C.softTeal);
  bullet(slide, ctx, "문제 재정의: 한국어 개인정보와 보안 오탐 문제로 범위 조정", 104, 292, 400);
  bullet(slide, ctx, "Colab 실험: 데이터 생성, 학습, 평가, 오류 분석을 반복 실행", 104, 352, 400);
  bullet(slide, ctx, "디버깅: hard-negative FPR 0의 의미를 재검증하고 과장 제거", 104, 412, 400);
  bullet(slide, ctx, "발표화: 평가 기준에 맞춰 메시지, 시연, 대본을 재구성", 104, 472, 400);

  table(
    slide,
    ctx,
    626,
    224,
    [220, 210, 180],
    [
      ["Evidence", "What it proves", "Count / path"],
      ["Git commits", "과정이 추적 가능함", "9 commits"],
      ["Synthetic dataset", "한국형 PII 학습 기반", "50k / 5k / 5k"],
      ["Eval sets", "정답 외 일반화 확인", "300 / 100 / 10"],
      ["Fine-tune checkpoint", "학습 저장 성공", "model.safetensors"],
      ["Final reports", "재현 가능한 결과", "results/*.md"],
    ],
    { rowH: 43 },
  );

  ctx.addShape(slide, { x: 92, y: 604, width: 1096, height: 40, fill: C.softAmber, line: { fill: C.softAmber, width: 1, style: "solid" } });
  smallText(slide, ctx, "질의응답 포인트: AI가 한 번에 답을 준 것이 아니라, 내가 평가 기준과 실패 사례를 계속 던져서 더 안전한 최종 구현으로 수렴시켰다고 설명합니다.", 118, 616, 1040, 18, 12.5, C.ink);
  footer(slide, ctx, 10);
  return slide;
}
