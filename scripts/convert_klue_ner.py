
from __future__ import annotations

import json
import random
from pathlib import Path

from datasets import load_dataset


PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
OUT_PATH = PROJECT_DIR / "data" / "processed" / "klue_ner_mapped_1000.jsonl"

random.seed(42)


def normalize_token(token: str) -> str:
    """Normalize KLUE token text."""
    return token.replace("▁", " ")


def bio_to_spans(tokens: list[str], tag_names: list[str], tag_ids: list[int]) -> tuple[str, list[dict]]:
    """Convert KLUE token BIO tags into character-offset spans."""
    text = "".join(normalize_token(token) for token in tokens).strip()
    spans = []

    cursor = 0
    current_label = None
    current_start = None
    current_end = None

    for token, tag_id in zip(tokens, tag_ids):
        piece = normalize_token(token)
        start = cursor
        end = cursor + len(piece)
        cursor = end

        tag = tag_names[tag_id]

        if tag == "O":
            if current_label is not None:
                spans.append({
                    "start": current_start,
                    "end": current_end,
                    "label": current_label,
                    "text": text[current_start:current_end],
                })
                current_label = None
                current_start = None
                current_end = None
            continue

        prefix, raw_label = tag.split("-", 1)

        if raw_label == "PS":
            mapped_label = "private_person"
        elif raw_label == "LC":
            mapped_label = "private_address"
        else:
            mapped_label = None

        if mapped_label is None:
            if current_label is not None:
                spans.append({
                    "start": current_start,
                    "end": current_end,
                    "label": current_label,
                    "text": text[current_start:current_end],
                })
                current_label = None
                current_start = None
                current_end = None
            continue

        if prefix == "B" or current_label != mapped_label:
            if current_label is not None:
                spans.append({
                    "start": current_start,
                    "end": current_end,
                    "label": current_label,
                    "text": text[current_start:current_end],
                })

            current_label = mapped_label
            current_start = start
            current_end = end
        else:
            current_end = end

    if current_label is not None:
        spans.append({
            "start": current_start,
            "end": current_end,
            "label": current_label,
            "text": text[current_start:current_end],
        })

    spans = [
        span for span in spans
        if span["text"].strip() and span["start"] < span["end"]
    ]

    return text, spans


def main() -> None:
    ds = load_dataset("klue", "ner")
    tag_names = ds["train"].features["ner_tags"].feature.names

    rows = []

    for split in ["train", "validation"]:
        for example in ds[split]:
            text, spans = bio_to_spans(
                tokens=example["tokens"],
                tag_names=tag_names,
                tag_ids=example["ner_tags"],
            )

            spans = [
                span for span in spans
                if span["label"] in {"private_person", "private_address"}
            ]

            if not spans:
                continue

            rows.append({
                "id": f"klue_{split}_{len(rows) + 1:05d}",
                "domain": "klue_ner",
                "text": text,
                "spans": spans,
            })

    random.shuffle(rows)
    rows = rows[:1000]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"[OK] wrote rows: {len(rows)}")
    print(f"[OK] output: {OUT_PATH}")


if __name__ == "__main__":
    main()
