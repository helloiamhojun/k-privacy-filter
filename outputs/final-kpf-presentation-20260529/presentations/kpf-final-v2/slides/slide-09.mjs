import { bg, title, footer, C, card, label, bullet, smallText } from "./common.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "Live Demonstration", "Colab에서 실제 필터를 실행하고 Gradio로 보여줍니다", "시연은 fine-tuned 단독 모델이 아니라, 최종 hybrid KPF 경로로 진행합니다.");

  card(slide, ctx, 70, 212, 390, 380, "#FFFFFF");
  label(slide, ctx, "실행 순서", 96, 238, 112, C.softBlue);
  bullet(slide, ctx, "Colab 노트북 접속 후 Drive mount 확인", 104, 296, 300);
  bullet(slide, ctx, "프로젝트 폴더로 이동: /content/drive/MyDrive/k-privacy-filter", 104, 348, 300);
  bullet(slide, ctx, "python scripts/demo.py 실행", 104, 410, 300);
  bullet(slide, ctx, "Gradio public URL을 열고 입력/결과 확인", 104, 462, 300);
  bullet(slide, ctx, "네트워크 오류 시 녹화 영상 또는 캡처 결과로 대체", 104, 514, 300);

  card(slide, ctx, 500, 212, 690, 380, "#FFFFFF");
  label(slide, ctx, "시연 입력 3개", 526, 238, 124, C.softTeal);
  smallText(slide, ctx, "1) 주소 + 이름 + API key", 530, 296, 220, 20, 12, C.ink);
  smallText(slide, ctx, "주소는 경기도 화성시 동탄역로 150 102동 3804호야. 그리고 내 이름은 최호준이고, api 키는 sk-...야.", 552, 320, 550, 32, 11, C.muted);
  smallText(slide, ctx, "기대: 주소, 이름, secret이 각각 <PRIVATE_...>로 마스킹", 552, 356, 500, 20, 10.5, C.green);

  smallText(slide, ctx, "2) 아이디 + 비밀번호", 530, 400, 220, 20, 12, C.ink);
  smallText(slide, ctx, "아이디는 chjspd고, 비밀번호는 chIghwns1011!@!이야.", 552, 424, 520, 24, 11, C.muted);
  smallText(slide, ctx, "기대: 비밀번호는 secret으로 마스킹, 아이디는 정책에 따라 계정 식별자로 처리", 552, 454, 560, 20, 10.5, C.green);

  smallText(slide, ctx, "3) Hard-negative", 530, 498, 220, 20, 12, C.ink);
  smallText(slide, ctx, "모델명은 900101-1234567-A입니다.", 552, 522, 520, 22, 11, C.muted);
  smallText(slide, ctx, "기대: 실제 주민번호가 아닌 코드형 문맥이면 마스킹하지 않음", 552, 550, 540, 20, 10.5, C.green);

  ctx.addShape(slide, { x: 94, y: 620, width: 1092, height: 36, fill: C.navy });
  smallText(slide, ctx, "시연 멘트: '이 화면은 정답을 외워서 맞히는 것이 아니라, 입력 문맥과 한국형 패턴을 동시에 확인하는 최종 KPF 경로입니다.'", 124, 630, 1032, 18, 12.5, "#FFFFFF");
  footer(slide, ctx, 9);
  return slide;
}
