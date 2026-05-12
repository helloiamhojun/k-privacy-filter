
from __future__ import annotations

import csv
import json
import time
from collections import Counter
from pathlib import Path

import torch
from opf import OPF
from seqeval.metrics import classification_report, f1_score, precision_score, recall_score


PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
EVAL_PATH = PROJECT_DIR / "data" / "raw" / "korean_eval_300.jsonl"
RESULTS_PATH = PROJECT_DIR / "results" / "results.csv"


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL dataset."""
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def spans_to_char_tags(text: str, spans: list[dict]) -> list[str]:
    """Convert character-offset spans to BIO tags."""
    tags = ["O"] * len(text)

    for span in spans:
        label = span["label"]
        start = span["start"]
        end = span["end"]

        if start >= end:
            continue

        tags[start] = f"B-{label}"
        for i in range(start + 1, end):
            tags[i] = f"I-{label}"

    return tags


def predict_spans(redactor: OPF, text: str) -> list[dict]:
    """Run OPF and normalize detected spans."""
    result = redactor.redact(text)
    spans = []

    for span in result.detected_spans:
        spans.append({
            "start": int(span.start),
            "end": int(span.end),
            "label": str(span.label),
            "text": str(span.text),
        })

    return spans


def exact_span_scores(gold_rows: list[dict], pred_rows: list[dict]) -> dict[str, float]:
    """Compute exact-match span precision, recall, and F1."""
    gold = []
    pred = []

    for row in gold_rows:
        for span in row["spans"]:
            gold.append((row["id"], span["start"], span["end"], span["label"]))

    for row in pred_rows:
        for span in row["predicted_spans"]:
            pred.append((row["id"], span["start"], span["end"], span["label"]))

    gold_set = set(gold)
    pred_set = set(pred)
    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "exact_precision": precision,
        "exact_recall": recall,
        "exact_f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def main() -> None:
    rows = load_jsonl(EVAL_PATH)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[INFO] rows={len(rows)} device={device}")
    redactor = OPF(device=device, output_mode="typed")

    y_true = []
    y_pred = []
    pred_rows = []

    start_time = time.perf_counter()

    for idx, row in enumerate(rows, start=1):
        text = row["text"]
        pred_spans = predict_spans(redactor, text)

        y_true.append(spans_to_char_tags(text, row["spans"]))
        y_pred.append(spans_to_char_tags(text, pred_spans))

        pred_rows.append({
            "id": row["id"],
            "domain": row["domain"],
            "text": text,
            "gold_spans": row["spans"],
            "predicted_spans": pred_spans,
        })

        if idx % 25 == 0:
            print(f"[BASELINE] processed {idx}/{len(rows)}")

    elapsed = time.perf_counter() - start_time

    seq_precision = precision_score(y_true, y_pred, zero_division=0)
    seq_recall = recall_score(y_true, y_pred, zero_division=0)
    seq_f1 = f1_score(y_true, y_pred, zero_division=0)
    exact = exact_span_scores(rows, pred_rows)

    print("\n[SEQEVAL]")
    print(f"precision={seq_precision:.4f}")
    print(f"recall={seq_recall:.4f}")
    print(f"f1={seq_f1:.4f}")

    print("\n[EXACT SPAN]")
    print(exact)

    print("\n[REPORT]")
    print(classification_report(y_true, y_pred, zero_division=0))

    print("\n[LATENCY]")
    print(f"total_seconds={elapsed:.2f}")
    print(f"seconds_per_example={elapsed / len(rows):.4f}")

    pred_path = PROJECT_DIR / "results" / "baseline_predictions.jsonl"
    pred_path.parent.mkdir(parents=True, exist_ok=True)

    with pred_path.open("w", encoding="utf-8") as f:
        for row in pred_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not RESULTS_PATH.exists()

    with RESULTS_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_name",
                "rows",
                "device",
                "seqeval_precision",
                "seqeval_recall",
                "seqeval_f1",
                "exact_precision",
                "exact_recall",
                "exact_f1",
                "tp",
                "fp",
                "fn",
                "total_seconds",
                "seconds_per_example",
            ],
        )

        if write_header:
            writer.writeheader()

        writer.writerow({
            "run_name": "baseline_openai_privacy_filter",
            "rows": len(rows),
            "device": device,
            "seqeval_precision": seq_precision,
            "seqeval_recall": seq_recall,
            "seqeval_f1": seq_f1,
            "exact_precision": exact["exact_precision"],
            "exact_recall": exact["exact_recall"],
            "exact_f1": exact["exact_f1"],
            "tp": exact["tp"],
            "fp": exact["fp"],
            "fn": exact["fn"],
            "total_seconds": elapsed,
            "seconds_per_example": elapsed / len(rows),
        })

    print(f"\n[OK] predictions: {pred_path}")
    print(f"[OK] results: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
