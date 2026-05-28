import { bg, C, COVER_IMAGE, metric } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "#F4F1E9");
  await ctx.addImage(slide, {
    path: COVER_IMAGE,
    x: 770,
    y: 0,
    width: 510,
    height: 720,
    fit: "cover",
    alt: "privacy shield abstract visual",
  });
  ctx.addShape(slide, { x: 0, y: 0, width: 820, height: 720, fill: "#F4F1E9" });
  ctx.addShape(slide, { x: 720, y: 0, width: 120, height: 720, fill: "#F4F1E9D9" });
  ctx.addText(slide, { text: "FINAL PRESENTATION", x: 64, y: 58, width: 260, height: 26, fontSize: 13, color: C.teal, bold: true, typeface: "Aptos" });
  ctx.addText(slide, { text: "K-Privacy Filter", x: 62, y: 120, width: 620, height: 70, fontSize: 46, color: C.ink, bold: true, typeface: "Aptos Display" });
  ctx.addText(slide, { text: "한국형 개인정보 필터 최종 구현과 평가", x: 64, y: 198, width: 650, height: 40, fontSize: 25, color: C.ink, bold: true, typeface: "Malgun Gothic" });
  ctx.addText(slide, {
    text: "OPF의 범용 탐지력에 한국형 Regex Safety Net과 문맥 기반 오탐 억제를 결합해, 라이브 데모가 가능한 개인정보 마스킹 시스템을 완성했습니다.",
    x: 66,
    y: 262,
    width: 610,
    height: 70,
    fontSize: 17,
    color: C.muted,
    typeface: "Malgun Gothic",
  });
  ctx.addShape(slide, { x: 64, y: 392, width: 618, height: 150, fill: "#FFFFFF", line: { fill: "#D9DEE4", width: 1, style: "solid" } });
  metric(slide, ctx, 88, 422, 150, "Eval300 F1", "0.6919", "보수적 최종 replay 기준", C.blue);
  metric(slide, ctx, 278, 422, 150, "Hard-neg FPR", "0.0000", "고정 100개 샘플 기준\n전체 FPR 0 아님", C.green);
  metric(slide, ctx, 468, 422, 150, "Adversarial F1", "0.9000", "우회형 10개 샘플", C.teal);
  ctx.addText(slide, { text: "2026-05-29 | Google Colab + Drive artifacts + local Git repository", x: 66, y: 660, width: 620, height: 24, fontSize: 11, color: "#7A8491", typeface: "Aptos" });
  return slide;
}
