import { bg, title, footer, C, card, label, bullet, metric, table, smallText } from "./common.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "Fine-tuning 실험", "학습은 정상 저장했지만, 최종 배포 후보로 쓰지는 않았습니다", "성공한 실험도 결과가 나쁘면 버리는 것이 보안 프로젝트에서는 더 전문적인 판단입니다.");

  card(slide, ctx, 70, 214, 480, 340, "#FFFFFF");
  label(slide, ctx, "완료한 것", 96, 238, 112, C.softGreen);
  bullet(slide, ctx, "한국형 개인정보 synthetic dataset 생성", 104, 294, 370);
  bullet(slide, ctx, "train 50,000 / val 5,000 / test 5,000", 104, 344, 370);
  bullet(slide, ctx, "DistilBERT multilingual token classifier 학습", 104, 394, 370);
  bullet(slide, ctx, "Colab Drive에 final/model.safetensors 저장 확인", 104, 444, 370);
  smallText(slide, ctx, "체크포인트: results/korean_pii_finetune/distilbert_mbert_20k_20260529_success/final", 104, 506, 390, 26, 10.5, C.muted);

  table(
    slide,
    ctx,
    615,
    222,
    [220, 140, 140, 140],
    [
      ["Fine-tuned standalone", "Exact F1", "Empty-row FPR", "판단"],
      ["Synthetic test 5000", "0.9912", "0.0000", "과적합 가능"],
      ["Eval300", "0.6052", "0.0000", "최종 KPF보다 낮음"],
      ["Hard-negative 100", "0.0000", "0.5700", "오탐 위험"],
      ["Adversarial 10", "0.2000", "-", "우회 취약"],
    ],
    { rowH: 45 },
  );

  card(slide, ctx, 682, 500, 430, 90, C.softRed, C.softRed);
  metric(slide, ctx, 708, 516, 145, "Deploy decision", "보류", "단독 모델은 시연 기준 미달", C.red);
  smallText(slide, ctx, "최종 발표 메시지: fine-tuning은 연구 트랙으로 보관하고, 실제 데모는 hybrid KPF로 진행합니다.", 870, 526, 210, 38, 12, C.ink);

  footer(slide, ctx, 8);
  return slide;
}
