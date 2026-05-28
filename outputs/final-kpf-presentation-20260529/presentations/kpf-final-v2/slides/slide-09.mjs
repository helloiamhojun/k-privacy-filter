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
  label(slide, ctx, "시연 입력 4개", 526, 238, 124, C.softTeal);
  smallText(slide, ctx, "1) 계정 + 학번 + 지번 주소", 530, 292, 260, 20, 12, C.ink);
  smallText(slide, ctx, "내 아이디는 chjspd이고, 비밀번호는 32215116이고, 내 학번은 32215116이고, 내 집 주소는 경기도 용인시 수지구 1336-2야.", 552, 316, 570, 34, 10.5, C.muted);
  smallText(slide, ctx, "기대: 아이디, 비밀번호, 학번, 지번 주소가 마스킹", 552, 356, 500, 20, 10.5, C.green);

  smallText(slide, ctx, "2) 인증·네트워크 정보", 530, 396, 260, 20, 12, C.ink);
  smallText(slide, ctx, "OTP는 123456이고, 접속 IP는 192.168.0.15, MAC주소는 AA:BB:CC:DD:EE:FF입니다.", 552, 420, 560, 24, 10.5, C.muted);
  smallText(slide, ctx, "기대: OTP, IP, MAC이 각각 마스킹", 552, 450, 560, 20, 10.5, C.green);

  smallText(slide, ctx, "3) Hard-negative", 530, 492, 220, 20, 12, C.ink);
  smallText(slide, ctx, "모델명은 900101-1234567-A입니다. 문서 버전은 sk-proj-example-not-real로 표시했습니다.", 552, 516, 560, 26, 10.5, C.muted);
  smallText(slide, ctx, "기대: 실제 개인정보가 아닌 반례는 의도적으로 마스킹하지 않음", 552, 548, 540, 20, 10.5, C.green);

  ctx.addShape(slide, { x: 94, y: 620, width: 1092, height: 36, fill: C.navy });
  smallText(slide, ctx, "시연 멘트: '이 화면은 정답을 외워서 맞히는 것이 아니라, 입력 문맥과 한국형 패턴을 동시에 확인하는 최종 KPF 경로입니다.'", 124, 630, 1032, 18, 12.5, "#FFFFFF");
  footer(slide, ctx, 9);
  return slide;
}
