import { bg, title, footer, C, card, bullet, smallText } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "문제 정의", "한국어 개인정보는 범용 필터만으로는 놓치거나 과하게 잡힙니다", "주소, 계좌, 주민번호, 비밀번호, API key가 채팅과 로그에 섞이면 보안 사고로 바로 이어질 수 있습니다.");
  card(slide, ctx, 70, 214, 520, 310, "#FFFFFF");
  ctx.addText(slide, { text: "입력 예시", x: 96, y: 238, width: 200, height: 26, fontSize: 16, bold: true, color: C.ink, typeface: "Malgun Gothic" });
  smallText(slide, ctx, "주소는 경기도 화성시 동탄역로 150 102동 3804호야.\n내 이름은 최호준이고, api 키는 sk-... 이야.\n아이디는 chjspd고, 비밀번호는 chIghwns1011!@!이야.", 96, 286, 450, 110, 16, C.dark);
  ctx.addShape(slide, { x: 96, y: 430, width: 420, height: 1, fill: C.line });
  smallText(slide, ctx, "보안 관점의 위험: 사용자가 무심코 입력한 민감 정보가 LLM 요청, 로그, 화면 공유, 저장소에 남을 수 있음", 96, 456, 430, 44, 13, C.red);
  card(slide, ctx, 650, 214, 560, 310, "#FFFFFF");
  ctx.addText(slide, { text: "왜 한국형 보강이 필요한가", x: 678, y: 238, width: 300, height: 26, fontSize: 16, bold: true, color: C.ink, typeface: "Malgun Gothic" });
  bullet(slide, ctx, "한국 주소는 행정구역, 도로명, 동/호수, 조사까지 붙어 경계가 복잡함", 684, 286, 470);
  bullet(slide, ctx, "전화번호와 계좌번호는 숫자 패턴이 비슷해 라벨 혼동이 잦음", 684, 356, 470);
  bullet(slide, ctx, "예시값, 상품코드, 모델명은 개인정보처럼 보이지만 masking하면 오탐", 684, 426, 470);
  footer(slide, ctx, 3);
  return slide;
}
