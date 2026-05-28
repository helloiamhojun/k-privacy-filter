import { bg, title, footer, C, card, label, metric, table, smallText } from "./common.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "평가 결과", "최종 KPF는 단순 F1보다 오탐 통제까지 함께 개선했습니다", "숫자는 모두 재현 가능한 offline replay 기준이며, hard-negative 0은 고정 샘플 100개에서만 의미합니다.");

  table(
    slide,
    ctx,
    70,
    218,
    [260, 145, 145, 145, 145, 145],
    [
      ["System / Set", "Precision", "Recall", "Exact F1", "Covered R", "False Positive"],
      ["Baseline OPF / Eval300", "0.6716", "0.5332", "0.5945", "-", "0.3284 FPR"],
      ["Existing hybrid / Eval300", "0.7471", "0.6090", "0.6710", "0.7796", "87 FP"],
      ["Final KPF / Eval300", "0.7994", "0.6706", "0.7294", "0.8009", "71 FP"],
    ],
    { rowH: 48 },
  );

  card(slide, ctx, 96, 456, 322, 128, "#FFFFFF");
  metric(slide, ctx, 126, 476, 260, "Eval300 F1", "+0.1349", "baseline OPF 대비\n0.5945 -> 0.7294", C.blue);
  card(slide, ctx, 479, 456, 322, 128, "#FFFFFF");
  metric(slide, ctx, 509, 476, 260, "Hard-negative 100", "0 / 100", "final KPF가 flag한 샘플 수\n전체 FPR 0 주장 아님", C.green);
  card(slide, ctx, 862, 456, 322, 128, "#FFFFFF");
  metric(slide, ctx, 892, 476, 260, "Adversarial 10", "0.9000", "우회형 입력 exact F1", C.teal);

  label(slide, ctx, "발표 방어 문장", 92, 616, 140, C.softAmber);
  smallText(slide, ctx, "Hard-negative FPR 0은 정해진 100개 샘플에서의 결과입니다. 모델명·문서 버전·example-not-real은 개인정보가 아니므로 의도적으로 마스킹하지 않습니다.", 252, 619, 860, 26, 12.5, C.ink);
  footer(slide, ctx, 7);
  return slide;
}
