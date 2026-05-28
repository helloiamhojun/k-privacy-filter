
from __future__ import annotations

import sys
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


def redact(text: str) -> tuple[str, pd.DataFrame]:
    """Run K-Privacy hybrid redaction for Gradio."""
    if not text.strip():
        return "", pd.DataFrame(columns=["source", "label", "text", "start", "end"])

    result = PIPELINE.redact(text)

    rows = []
    for span in result["spans"]:
        rows.append({
            "source": span["source"],
            "label": span["label"],
            "text": span["text"],
            "start": span["start"],
            "end": span["end"],
        })

    df = pd.DataFrame(rows, columns=["source", "label", "text", "start", "end"])
    return result["masked_text"], df


examples = [
    ["김민수 주민번호는 900101-1234567이고 전화는 010-1234-5678입니다."],
    ["아이디는 chjspd고, 비밀번호는 chIghwns1011!@!이야."],
    ["주소는 경기도 화성시 동탄역로 150 102동 3804호야. 그리고 내 이름은 최호준이고, api 키는 sk-s129slkdjflksjflkdjf83slkdjflskj4e398i야."],
    ["계좌번호는 110-123-456789이고 카드번호는 1234-5678-9012-3456입니다."],
    ["여권번호는 M12345678이고 운전면허번호는 12-34-567890-12입니다."],
    ["사업자번호는 123-45-67890이고 법인등록번호는 110111-1234567입니다."],
    ["API_KEY=sk-proj-AbCdEf1234567890abcdef 토큰 삭제하고 박서연에게 메일 보내."],
    ["최유진 주소가 서울특별시 강남구 테헤란로 123 맞아?"],
]

with gr.Blocks(title="K-Privacy Filter") as demo:
    gr.Markdown("# K-Privacy Filter")
    gr.Markdown("OpenAI Privacy Filter + Korean Regex Safety Net")

    with gr.Row():
        input_text = gr.Textbox(
            label="Input text",
            lines=8,
            placeholder="개인정보가 포함된 한국어 문장을 입력하세요.",
        )

    run_btn = gr.Button("Redact", variant="primary")

    output_text = gr.Textbox(
        label="Masked text",
        lines=8,
    )

    spans_table = gr.Dataframe(
        label="Detected spans",
        headers=["source", "label", "text", "start", "end"],
        interactive=False,
    )

    gr.Examples(
        examples=examples,
        inputs=input_text,
    )

    run_btn.click(
        fn=redact,
        inputs=input_text,
        outputs=[output_text, spans_table],
    )

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
