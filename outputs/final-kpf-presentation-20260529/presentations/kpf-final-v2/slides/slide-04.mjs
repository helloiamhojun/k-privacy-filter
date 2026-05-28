import { bg, title, footer, C, flowBox, arrow, card, smallText } from "./common.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "최종 시스템 아키텍처", "OPF + Korean Regex Safety Net + 문맥 오탐 억제", "모델 하나에 모든 책임을 맡기지 않고, 규칙과 문맥 필터를 결합한 방어적 구조를 선택했습니다.");
  const y = 238;
  flowBox(slide, ctx, 58, y, 180, "1. Input", "채팅/로그/문서 텍스트\n한국어와 코드형 secret 혼재", C.softBlue);
  flowBox(slide, ctx, 280, y, 180, "2. OPF", "openai/privacy-filter\n범용 PII span 탐지", "#FFFFFF");
  flowBox(slide, ctx, 502, y, 205, "3. Regex Safety Net", "주민번호, 주소, 전화번호,\nAPI key, 계좌, 여권 등 보강", C.softTeal);
  flowBox(slide, ctx, 750, y, 205, "4. Context Filter", "예시, 모델명, 주문번호,\nplaceholder 문맥 오탐 제거", C.softAmber);
  flowBox(slide, ctx, 998, y, 205, "5. Merge & Mask", "overlap 병합 후\n<PRIVATE_...> 치환", C.softGreen);
  arrow(slide, ctx, 242, y + 46, 276, y + 46);
  arrow(slide, ctx, 464, y + 46, 498, y + 46);
  arrow(slide, ctx, 711, y + 46, 746, y + 46);
  arrow(slide, ctx, 959, y + 46, 994, y + 46);
  card(slide, ctx, 118, 440, 1044, 116, "#FFFFFF");
  ctx.addText(slide, { text: "핵심 구현 파일", x: 148, y: 462, width: 180, height: 24, fontSize: 15, bold: true, color: C.ink, typeface: "Malgun Gothic" });
  smallText(slide, ctx, "scripts/pipeline.py: OPF 결과와 regex 결과 병합\nscripts/regex_safety_net.py: 한국형 패턴, 문맥 false-positive suppression\nscripts/demo.py: Gradio live demo\nscripts/evaluate_final_kpf_offline.py: 재현 가능한 최종 평가", 148, 498, 900, 48, 12, C.muted);
  footer(slide, ctx, 4);
  return slide;
}
