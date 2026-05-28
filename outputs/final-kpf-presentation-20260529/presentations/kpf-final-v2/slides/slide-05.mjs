import { bg, title, footer, C, card, label, bullet, smallText } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "핵심 알고리즘", "정규식은 단순 보정이 아니라, 모델의 실패 영역을 맡는 안전망입니다", "최종 KPF는 span 탐지, 오탐 억제, 병합 우선순위를 분리해 안정성을 확보했습니다.");
  const cols = [
    ["탐지 보강", C.softTeal, ["주민/외국인등록번호", "사업자/법인번호", "전화번호/계좌/카드", "도로명·지번 주소", "API key·Slack token"]],
    ["문맥 억제", C.softAmber, ["예시, 샘플, 더미", "상품코드, 모델명", "주문번호, 버전번호", "placeholder", "문서 템플릿"]],
    ["병합 정책", C.softBlue, ["regex span 우선", "overlap 중복 제거", "주소 끝 조사 trim", "typed placeholder", "평가용 span 보존"]],
  ];
  cols.forEach((col, i) => {
    const x = 82 + i * 385;
    card(slide, ctx, x, 220, 330, 330, "#FFFFFF");
    label(slide, ctx, col[0], x + 22, 244, 130, col[1]);
    col[2].forEach((b, bi) => bullet(slide, ctx, b, x + 34, 302 + bi * 42, 250));
  });
  ctx.addShape(slide, { x: 116, y: 590, width: 1048, height: 46, fill: C.dark });
  smallText(slide, ctx, "설계 원칙: 민감한 정보는 놓치지 않되, 예시·코드·모델명처럼 실제 개인정보가 아닌 값은 가능한 한 제거한다.", 146, 603, 988, 22, 14, "#FFFFFF");
  footer(slide, ctx, 5);
  return slide;
}
