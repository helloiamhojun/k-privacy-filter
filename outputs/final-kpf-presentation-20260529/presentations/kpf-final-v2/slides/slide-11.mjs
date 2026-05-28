import { bg, title, footer, C, card, label, bullet, smallText } from "./common.mjs";

export async function slide11(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "한계점 및 향후 과제", "보안 시스템은 '잘 맞춘 예시'보다 실패 조건을 공개하는 쪽이 더 강합니다", "이번 프로젝트의 핵심 인사이트는 precision, recall, 오탐 억제를 함께 관리해야 한다는 것입니다.");

  const cols = [
    ["현재 한계", C.softRed, [
      "synthetic 데이터와 실제 사용자 데이터 사이의 분포 차이",
      "규칙형 탐지는 새로운 표현이 나오면 계속 확장 필요",
      "hard-negative 0은 고정 100개 샘플 기준",
      "Colab/Gradio 환경은 네트워크와 런타임 상태에 영향을 받음",
    ]],
    ["개선 방향", C.softBlue, [
      "공식 범주 기반 rule-pack을 지속 확장",
      "hard-negative를 평가 게이트로 고정해 regression 방지",
      "regex 이후 LLM/분류기 기반 context verifier 추가",
      "CI에서 Eval300, hard-negative, adversarial replay 자동화",
    ]],
    ["보안 인사이트", C.softGreen, [
      "개인정보 필터는 과소탐과 과대탐이 모두 위험",
      "모델 성능표 하나보다 실패 사례 분석이 더 중요",
      "한국형 PII는 고유식별정보뿐 아니라 계정·인증·네트워크 정보까지 봐야 함",
      "최종 산출물은 '완벽한 모델'이 아니라 검증 가능한 방어 체계",
    ]],
  ];

  cols.forEach((col, i) => {
    const x = 64 + i * 405;
    card(slide, ctx, x, 214, 360, 390, "#FFFFFF");
    label(slide, ctx, col[0], x + 22, 238, 122, col[1]);
    col[2].forEach((b, bi) => bullet(slide, ctx, b, x + 28, 298 + bi * 70, 300));
  });

  ctx.addShape(slide, { x: 98, y: 626, width: 1084, height: 34, fill: C.dark });
  smallText(slide, ctx, "마무리 문장: 이번 결과는 '한국형 개인정보 필터를 실전 평가 기준으로 다듬는 방법'을 보여준 프로젝트입니다.", 128, 635, 1024, 16, 12.5, "#FFFFFF");
  footer(slide, ctx, 11);
  return slide;
}
