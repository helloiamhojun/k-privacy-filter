import { bg, title, footer, C, card, label, bullet, smallText } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "핵심 알고리즘", "한국형 Privacy Rule Pack은 모델의 실패 영역을 맡는 안전망입니다", "공식 개인정보 범주를 기준으로 탐지 범위를 넓히고, hard-negative 문맥은 의도적으로 억제했습니다.");
  const cols = [
    ["탐지 보강", C.softTeal, ["고유식별정보", "주소·전화·이메일", "계좌·카드·CVC·OTP", "학번·사번·회원번호", "IP·MAC·GPS·URL"]],
    ["문맥 억제", C.softAmber, ["example/not-real", "상품코드·모델명", "주문번호·문서 버전", "placeholder·mock", "hard-negative 100"]],
    ["검증 정책", C.softBlue, ["regex span 우선", "overlap 중복 제거", "Eval300 replay", "hard-negative gate", "adversarial replay"]],
  ];
  cols.forEach((col, i) => {
    const x = 82 + i * 385;
    card(slide, ctx, x, 220, 330, 330, "#FFFFFF");
    label(slide, ctx, col[0], x + 22, 244, 130, col[1]);
    col[2].forEach((b, bi) => bullet(slide, ctx, b, x + 34, 302 + bi * 42, 250));
  });
  ctx.addShape(slide, { x: 116, y: 590, width: 1048, height: 46, fill: C.dark });
  smallText(slide, ctx, "설계 원칙: 민감한 정보는 넓게 잡되, 문서 버전·모델명·example-not-real처럼 실제 개인정보가 아닌 값은 의도적으로 제외한다.", 146, 603, 988, 22, 14, "#FFFFFF");
  footer(slide, ctx, 5);
  return slide;
}
