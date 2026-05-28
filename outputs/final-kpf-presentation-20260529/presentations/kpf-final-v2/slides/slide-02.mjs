import { bg, title, footer, C, card, label, bullet } from "./common.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "오늘의 주장", "평가 기준에 맞춘 핵심 메시지", "이전 발표 내용은 줄이고, 최종 구현체와 검증 결과 중심으로 압축합니다.");
  const xs = [70, 365, 660, 955];
  const heads = ["Creativity", "Completeness", "AI-Collaboration", "Professionalism"];
  const fills = [C.softTeal, C.softBlue, C.softGreen, C.softAmber];
  const bodies = [
    ["한국어 주소, 주민번호, 계좌, API key 등 국내형 PII를 별도 안전망으로 보강", "보안 문제를 생성형 AI 사용 흐름과 연결"],
    ["Colab에서 실제 OPF 추론, Regex 병합, Gradio 시연, 평가 파일 저장까지 완료", "hard-negative와 adversarial 평가로 과장 방지"],
    ["AI에게 실험 설계, 코드 수정, 오류 분석, PPT 작성까지 단계적으로 디렉팅", "fine-tuning 실패와 성공 모두 근거로 남김"],
    ["실제 동작 시연, 숫자의 범위 설명, 한계 인정, 다음 개선 과제 제시", "질의응답에서 방어 가능한 메시지로 구성"],
  ];
  xs.forEach((x, i) => {
    card(slide, ctx, x, 218, 235, 330, "#FFFFFF");
    label(slide, ctx, heads[i], x + 18, 238, 130, fills[i]);
    bullet(slide, ctx, bodies[i][0], x + 22, 292, 188);
    bullet(slide, ctx, bodies[i][1], x + 22, 382, 188);
  });
  ctx.addShape(slide, { x: 86, y: 590, width: 1108, height: 46, fill: C.navy });
  ctx.addText(slide, {
    text: "한 줄 결론: 최종 배포 후보는 fine-tuned 단독 모델이 아니라, 실전 오탐을 줄인 Hybrid KPF입니다.",
    x: 112,
    y: 604,
    width: 1056,
    height: 24,
    fontSize: 15,
    bold: true,
    color: "#FFFFFF",
    align: "center",
    typeface: "Malgun Gothic",
  });
  footer(slide, ctx, 2);
  return slide;
}
