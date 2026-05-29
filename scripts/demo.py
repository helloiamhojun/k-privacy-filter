from __future__ import annotations

import html
import inspect
import re
import sys
from collections import Counter
from pathlib import Path

import gradio as gr
import pandas as pd
import torch

PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
SCRIPT_DIR = PROJECT_DIR / "scripts"
sys.path.append(str(SCRIPT_DIR))

from pipeline import KPrivacyPipeline


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[INFO] loading pipeline on {DEVICE}")
PIPELINE = KPrivacyPipeline(device=DEVICE)
print("[INFO] pipeline loaded")


LABEL_META = {
    "private_person": ("Person", "person"),
    "private_address": ("Address", "home_pin"),
    "private_email": ("Email", "alternate_email"),
    "private_phone": ("Phone", "call"),
    "private_url": ("URL", "link"),
    "private_date": ("Date", "calendar_month"),
    "private_network": ("Network", "router"),
    "private_location": ("Location", "my_location"),
    "account_number": ("Account", "account_balance"),
    "secret": ("Secret", "key"),
}

HARD_NEGATIVE_HINTS = [
    "모델명",
    "문서 버전",
    "상품코드",
    "주문번호",
    "example",
    "not-real",
    "placeholder",
    "dummy",
]


def render_masked_html(masked_text: str) -> str:
    """Render placeholders as dashboard badges."""
    escaped = html.escape(masked_text)

    def repl(match: re.Match[str]) -> str:
        label = match.group(1).lower()
        title, icon = LABEL_META.get(label, (label.replace("_", " ").title(), "shield"))
        return (
            f'<span class="kpf-token kpf-token-{label}">'
            f'<span class="material-symbols-outlined">{icon}</span>'
            f'&lt;{match.group(1)}&gt;'
            f'<small>{html.escape(title)}</small>'
            f"</span>"
        )

    annotated = re.sub(r"&lt;([A-Z_]+)&gt;", repl, escaped)
    return f'<div class="masked-result">{annotated}</div>'


def render_summary(rows: list[dict[str, object]], text: str) -> str:
    labels = Counter(str(row["label"]) for row in rows)
    sources = Counter(str(row["source"]) for row in rows)
    label_chips = "".join(
        f'<span class="summary-chip">{html.escape(LABEL_META.get(label, (label, ""))[0])}: {count}</span>'
        for label, count in labels.most_common()
    ) or '<span class="summary-chip muted">No entities</span>'
    source_chips = "".join(
        f'<span class="summary-chip source">{html.escape(source)}: {count}</span>'
        for source, count in sources.most_common()
    ) or '<span class="summary-chip source">No source</span>'
    hard_negative = not rows and any(marker.lower() in text.lower() for marker in HARD_NEGATIVE_HINTS)
    note_title = "Hard-negative suppressed" if hard_negative else "Hybrid scan complete"
    note_body = (
        "개인정보처럼 보이지만 모델명, 문서 버전, example/not-real 문맥이라 의도적으로 마스킹하지 않았습니다."
        if hard_negative
        else "OPF 후보와 한국형 Privacy Rule Pack 결과를 병합하고 문맥 기반 오탐 억제를 적용했습니다."
    )
    return f"""
    <div class="summary-grid">
      <div class="summary-card">
        <span class="summary-label">Entities</span>
        <strong>{len(rows)}</strong>
      </div>
      <div class="summary-card">
        <span class="summary-label">Device</span>
        <strong>{html.escape(DEVICE.upper())}</strong>
      </div>
      <div class="summary-wide">
        <span class="summary-label">Labels</span>
        <div class="chip-row">{label_chips}</div>
      </div>
      <div class="summary-wide">
        <span class="summary-label">Sources</span>
        <div class="chip-row">{source_chips}</div>
      </div>
    </div>
    <div class="hard-note">
      <div class="hard-note-icon">i</div>
      <div>
        <strong>{note_title}</strong>
        <p>{note_body}</p>
      </div>
    </div>
    """


def redact(text: str) -> tuple[str, pd.DataFrame, str]:
    """Run K-Privacy hybrid redaction for Gradio."""
    columns = ["source", "label", "text", "start", "end"]
    if not text.strip():
        empty = pd.DataFrame(columns=columns)
        return render_masked_html(""), empty, render_summary([], text)

    result = PIPELINE.redact(text)

    rows = []
    for span in result["spans"]:
        rows.append(
            {
                "source": span["source"],
                "label": span["label"],
                "text": span["text"],
                "start": span["start"],
                "end": span["end"],
            }
        )

    df = pd.DataFrame(rows, columns=columns)
    return render_masked_html(result["masked_text"]), df, render_summary(rows, text)


def clear() -> tuple[str, str, pd.DataFrame, str]:
    columns = ["source", "label", "text", "start", "end"]
    return "", render_masked_html(""), pd.DataFrame(columns=columns), render_summary([], "")


examples = [
    ["내 아이디는 chjspd이고, 비밀번호는 32215116이고, 내 학번은 32215116이고, 내 집 주소는 경기도 용인시 수지구 1336-2야."],
    ["OTP는 123456이고, 접속 IP는 192.168.0.15, MAC주소는 AA:BB:CC:DD:EE:FF입니다."],
    ["주소는 경기도 화성시 동탄역로 150 102동 3804호야. 그리고 내 이름은 최호준이고, api 키는 sk-s129slkdjflksjflkdjf83slkdjflskj4e398i야."],
    ["계좌번호는 110-123-456789이고 카드번호는 1234-5678-9012-3456입니다."],
    ["모델명은 900101-1234567-A입니다."],
    ["문서 버전은 sk-proj-example-not-real로 표시했습니다."],
]


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Material+Symbols+Outlined');

:root {
  --kpf-bg: #f7f9fb;
  --kpf-surface: #ffffff;
  --kpf-surface-low: #f2f4f6;
  --kpf-surface-mid: #e8edf3;
  --kpf-line: #d6dbe3;
  --kpf-ink: #17202a;
  --kpf-muted: #5f6874;
  --kpf-primary: #173a66;
  --kpf-primary-2: #315f9d;
  --kpf-blue-soft: #dbe8ff;
  --kpf-green: #0b7a53;
  --kpf-green-soft: #dcf5eb;
  --kpf-purple: #6741a5;
  --kpf-purple-soft: #ece2ff;
  --kpf-amber-soft: #fff0d7;
}

body, .gradio-container {
  background: var(--kpf-bg) !important;
  color: var(--kpf-ink) !important;
  font-family: Inter, "Malgun Gothic", system-ui, sans-serif !important;
}

.gradio-container {
  max-width: none !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
}

.sidebar {
  min-height: 100vh;
  background: #eef2f6;
  border-right: 1px solid var(--kpf-line);
  padding: 24px 16px;
  color: var(--kpf-ink) !important;
}

.brand-block {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 28px;
}

.brand-mark {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: #d7e7ff;
  background: var(--kpf-primary);
  font-weight: 800;
}

.brand-title {
  font-size: 18px;
  font-weight: 800;
  line-height: 22px;
  color: var(--kpf-primary) !important;
}

.brand-subtitle, .nav-caption {
  color: var(--kpf-muted);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .05em;
  text-transform: uppercase;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  color: var(--kpf-muted);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: .05em;
  text-transform: uppercase;
}

.nav-item .material-symbols-outlined {
  color: currentColor !important;
  opacity: 1 !important;
}

.nav-item.active {
  color: #ffffff !important;
  background: var(--kpf-primary);
}

.nav-footer {
  margin-top: 40px;
  padding-top: 18px;
  border-top: 1px solid var(--kpf-line);
}

.workspace {
  min-width: 0;
  padding: 0 28px 28px;
  overflow-x: hidden;
}

.topbar {
  height: 66px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--kpf-line);
  margin: 0 -28px 24px;
  padding: 0 28px;
  background: rgba(247, 249, 251, .94);
}

.topbar-title {
  font-size: 24px;
  font-weight: 800;
  color: var(--kpf-primary);
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--kpf-surface-low);
  border: 1px solid var(--kpf-line);
  border-radius: 999px;
  padding: 8px 12px;
  color: var(--kpf-muted);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .04em;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #39d99a;
}

.panel {
  background: var(--kpf-surface);
  border: 1px solid var(--kpf-line);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 26px rgba(18, 35, 55, .05);
  color: var(--kpf-ink) !important;
}

.panel-header {
  border-bottom: 1px solid var(--kpf-line);
  padding: 13px 16px;
  background: #fbfcfd;
  color: var(--kpf-primary);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.panel-body {
  padding: 16px;
}

.kpf-input textarea {
  min-height: 240px !important;
  border: 0 !important;
  box-shadow: none !important;
  font-size: 16px !important;
  line-height: 1.55 !important;
  background: #ffffff !important;
  color: var(--kpf-ink) !important;
  -webkit-text-fill-color: var(--kpf-ink) !important;
  caret-color: var(--kpf-primary) !important;
}

.kpf-input textarea::placeholder {
  color: #8a93a0 !important;
  -webkit-text-fill-color: #8a93a0 !important;
}

.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 12px;
}

.kpf-btn-primary {
  background: var(--kpf-primary) !important;
  border: 0 !important;
  border-radius: 8px !important;
  color: white !important;
  font-weight: 800 !important;
}

.kpf-btn-secondary {
  background: var(--kpf-surface-mid) !important;
  border: 1px solid var(--kpf-line) !important;
  border-radius: 8px !important;
  color: var(--kpf-muted) !important;
  font-weight: 800 !important;
}

.masked-result {
  min-height: 240px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 16px;
  line-height: 1.7;
  padding: 8px 2px 48px;
  background: #ffffff !important;
  color: var(--kpf-ink) !important;
  -webkit-text-fill-color: var(--kpf-ink) !important;
  opacity: 1 !important;
}

.kpf-output,
.kpf-summary,
.kpf-summary * {
  color: var(--kpf-ink) !important;
  opacity: 1 !important;
}

.kpf-token {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border-radius: 6px;
  padding: 2px 6px;
  margin: 0 1px;
  border: 1px solid var(--kpf-line);
  font-family: "JetBrains Mono", monospace;
  font-size: 13px;
  font-weight: 700;
}

.kpf-token small {
  color: inherit;
  opacity: .68;
  font-family: Inter, sans-serif;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}

.kpf-token .material-symbols-outlined {
  font-size: 15px;
}

.kpf-token-private_person, .kpf-token-private_address, .kpf-token-private_email, .kpf-token-private_phone {
  background: var(--kpf-blue-soft);
  color: var(--kpf-primary) !important;
  border-color: #adc7f7;
  -webkit-text-fill-color: var(--kpf-primary) !important;
}

.kpf-token-account_number, .kpf-token-secret {
  background: var(--kpf-purple-soft);
  color: var(--kpf-purple) !important;
  border-color: #cab8ff;
  -webkit-text-fill-color: var(--kpf-purple) !important;
}

.kpf-token-private_network, .kpf-token-private_location, .kpf-token-private_url, .kpf-token-private_date {
  background: var(--kpf-green-soft);
  color: var(--kpf-green) !important;
  border-color: #9bddc3;
  -webkit-text-fill-color: var(--kpf-green) !important;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.summary-card, .summary-wide {
  background: var(--kpf-surface);
  border: 1px solid var(--kpf-line);
  border-radius: 10px;
  padding: 14px;
}

.summary-wide {
  grid-column: 1 / -1;
}

.summary-label {
  display: block;
  color: var(--kpf-muted);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.summary-card strong {
  display: block;
  font-size: 30px;
  color: var(--kpf-primary);
  line-height: 34px;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.summary-chip {
  display: inline-flex;
  border-radius: 999px;
  background: var(--kpf-blue-soft);
  color: var(--kpf-primary);
  padding: 5px 9px;
  font-size: 12px;
  font-weight: 800;
}

.summary-chip.source {
  background: var(--kpf-green-soft);
  color: var(--kpf-green);
}

.summary-chip.muted {
  background: var(--kpf-surface-mid);
  color: var(--kpf-muted);
}

.hard-note {
  display: flex;
  gap: 12px;
  background: var(--kpf-amber-soft);
  border-left: 4px solid #d69b2d;
  border-radius: 0 12px 12px 0;
  padding: 14px;
  margin-top: 14px;
}

.hard-note-icon {
  width: 24px;
  height: 24px;
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: var(--kpf-primary);
  color: white;
  font-weight: 800;
  font-family: "JetBrains Mono", monospace;
}

.hard-note p {
  color: var(--kpf-muted);
  margin: 4px 0 0;
  line-height: 1.45;
}

.examples-wrap {
  margin: 4px 0 20px;
  color: var(--kpf-ink) !important;
}

.examples-wrap button,
.examples-wrap button * {
  background: #ffffff !important;
  color: var(--kpf-ink) !important;
  opacity: 1 !important;
  -webkit-text-fill-color: var(--kpf-ink) !important;
}

.gradio-dataframe {
  border-radius: 12px !important;
  overflow: hidden !important;
}

@media (max-width: 960px) {
  .app-shell {
    grid-template-columns: 1fr;
  }
  .sidebar {
    min-height: auto;
  }
  .workspace {
    padding: 0 16px 20px;
  }
}
"""


blocks_kwargs = {"title": "K-Privacy Filter Dashboard"}
if "css" in inspect.signature(gr.Blocks).parameters:
    blocks_kwargs["css"] = CSS


with gr.Blocks(**blocks_kwargs) as demo:
    with gr.Row(elem_classes=["app-shell"]):
        with gr.Column(scale=0, min_width=260, elem_classes=["sidebar"]):
            gr.HTML(
                """
                <div class="brand-block">
                  <div class="brand-mark">KP</div>
                  <div>
                    <div class="brand-title">K-Privacy Filter</div>
                    <div class="brand-subtitle">Precision PII Detection</div>
                  </div>
                </div>
                <div class="nav-item active"><span class="material-symbols-outlined">edit_note</span>Input</div>
                <div class="nav-item"><span class="material-symbols-outlined">analytics</span>Analysis</div>
                <div class="nav-item"><span class="material-symbols-outlined">description</span>Documentation</div>
                <div class="nav-footer">
                  <div class="nav-caption">Hybrid Pipeline</div>
                  <div class="nav-item"><span class="material-symbols-outlined">security</span>OPF Engine</div>
                  <div class="nav-item"><span class="material-symbols-outlined">rule</span>Rule Pack</div>
                  <div class="nav-item"><span class="material-symbols-outlined">verified_user</span>Context Filter</div>
                </div>
                """
            )
        with gr.Column(elem_classes=["workspace"]):
            gr.HTML(
                """
                <header class="topbar">
                  <div class="topbar-title">K-Privacy Filter Dashboard</div>
                  <div class="status-pill"><span class="status-dot"></span> Secure Hybrid Status</div>
                </header>
                """
            )
            with gr.Row(equal_height=True):
                with gr.Column(scale=1, elem_classes=["panel"]):
                    gr.HTML('<div class="panel-header">Input Analysis</div>')
                    with gr.Column(elem_classes=["panel-body"]):
                        input_text = gr.Textbox(
                            label="",
                            show_label=False,
                            lines=10,
                            placeholder="개인정보가 포함된 한국어 문장을 입력하세요. 예: 홍길동 고객님의 연락처는 010-1234-5678 입니다.",
                            elem_classes=["kpf-input"],
                        )
                        with gr.Row(elem_classes=["button-row"]):
                            clear_btn = gr.Button("Clear", elem_classes=["kpf-btn-secondary"])
                            run_btn = gr.Button("Redact", elem_classes=["kpf-btn-primary"])
                with gr.Column(scale=1, elem_classes=["panel"]):
                    gr.HTML('<div class="panel-header">Masked Result</div>')
                    with gr.Column(elem_classes=["panel-body"]):
                        output_html = gr.HTML(render_masked_html(""), elem_classes=["kpf-output"])
            with gr.Column(elem_classes=["examples-wrap"]):
                gr.Examples(examples=examples, inputs=input_text, label="Quick-Launch Test Cases")
            with gr.Row(equal_height=True):
                with gr.Column(scale=2, elem_classes=["panel"]):
                    gr.HTML('<div class="panel-header">Detection Spans</div>')
                    spans_table = gr.Dataframe(
                        label="",
                        show_label=False,
                        headers=["source", "label", "text", "start", "end"],
                        interactive=False,
                    )
                with gr.Column(scale=1):
                    summary_html = gr.HTML(render_summary([], ""), elem_classes=["kpf-summary"])

    run_btn.click(fn=redact, inputs=input_text, outputs=[output_html, spans_table, summary_html])
    clear_btn.click(fn=clear, inputs=None, outputs=[input_text, output_html, spans_table, summary_html])

if __name__ == "__main__":
    launch_kwargs = {"share": True, "debug": True}
    if "css" in inspect.signature(gr.Blocks.launch).parameters:
        launch_kwargs["css"] = CSS
    demo.launch(**launch_kwargs)
