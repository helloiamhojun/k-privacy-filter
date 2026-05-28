import { bg, footer, C, metric, card, smallText, label } from "./common.mjs";

export async function slide12(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "#F4F1E9");
  ctx.addText(slide, {
    text: "K-Privacy Filter",
    x: 76,
    y: 88,
    width: 780,
    height: 58,
    fontSize: 42,
    bold: true,
    color: C.ink,
    typeface: "Aptos Display",
  });
  ctx.addText(slide, {
    text: "한국형 개인정보를 더 안전하게 마스킹하기 위한 hybrid defense",
    x: 78,
    y: 158,
    width: 820,
    height: 36,
    fontSize: 20,
    bold: true,
    color: C.ink,
    typeface: "Malgun Gothic",
  });
  ctx.addText(slide, {
    text: "결론: 최종 구현체는 OPF의 범용 탐지력, 한국형 Regex Safety Net, 문맥 오탐 억제를 결합한 데모 가능한 시스템입니다. Fine-tuning은 저장까지 성공했지만, 현재는 연구 트랙으로 분리했습니다.",
    x: 80,
    y: 224,
    width: 1010,
    height: 72,
    fontSize: 17,
    color: C.muted,
    typeface: "Malgun Gothic",
  });

  card(slide, ctx, 86, 354, 320, 130, "#FFFFFF");
  metric(slide, ctx, 116, 384, 260, "Eval300 F1", "0.6919", "최종 KPF offline replay", C.blue);
  card(slide, ctx, 480, 354, 320, 130, "#FFFFFF");
  metric(slide, ctx, 510, 384, 260, "Hard-neg 100", "0 FP", "샘플 기준 오탐 제거", C.green);
  card(slide, ctx, 874, 354, 320, 130, "#FFFFFF");
  metric(slide, ctx, 904, 384, 260, "Adversarial F1", "0.9000", "우회형 입력 10개", C.teal);

  label(slide, ctx, "Q&A", 86, 548, 80, C.softAmber);
  smallText(slide, ctx, "예상 질문 답변 방향: hard-negative 0은 샘플 기준, fine-tuning은 보류, 최종 시연은 hybrid KPF, 다음 과제는 실제 데이터와 자동 평가 게이트입니다.", 184, 552, 900, 24, 13, C.ink);
  footer(slide, ctx, 12);
  return slide;
}
