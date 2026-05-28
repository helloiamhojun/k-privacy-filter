import { bg, title, footer, C, card, label, smallText } from "./common.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "구현체와 산출물", "코드는 Colab에서 실제 실행되고, 결과는 Drive와 repo에 남습니다", "라이브 데모와 평가 재현성을 분리해 발표 중 실패 리스크를 줄였습니다.");
  card(slide, ctx, 70, 220, 530, 350, "#FFFFFF");
  label(slide, ctx, "Runtime path", 96, 244, 130, C.softBlue);
  smallText(slide, ctx, "1. Google Colab 접속\n2. Drive mount: /content/drive/MyDrive/k-privacy-filter\n3. python scripts/demo.py\n4. Gradio public URL 생성\n5. 시연 입력 → 마스킹 결과 확인", 100, 304, 420, 140, 17, C.ink);
  ctx.addShape(slide, { x: 100, y: 486, width: 420, height: 44, fill: C.softAmber, line: { fill: C.softAmber, width: 1, style: "solid" } });
  smallText(slide, ctx, "Colab share 링크는 만료되므로 PPT에는 고정 URL을 넣지 않고, 현장에서 새 링크를 생성합니다.", 116, 498, 388, 22, 12, C.ink);
  card(slide, ctx, 660, 220, 530, 350, "#FFFFFF");
  label(slide, ctx, "Artifact map", 686, 244, 130, C.softTeal);
  smallText(slide, ctx, "results/final_kpf_experiments/\n  final_kpf_offline_report.md\n  final_kpf_offline_scores.json\n\nresults/korean_pii_finetune/\n  distilbert_mbert_20k_.../final/model.safetensors\n  eval_20260529/finetuned_eval_report.md\n\nresults/final_presentation/\n  최종 PPT, 대본, 시연 가이드", 690, 300, 430, 210, 12.5, C.ink);
  footer(slide, ctx, 6);
  return slide;
}
