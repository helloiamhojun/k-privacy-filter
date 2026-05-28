
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import torch
from opf import OPF
from seqeval.metrics import classification_report, f1_score, precision_score, recall_score

PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
SCRIPT_DIR = PROJECT_DIR / "scripts"
sys.path.append(str(SCRIPT_DIR))

from pipeline import Span, filter_contextual_spans, merge_spans, normalize_opf_spans
from regex_safety_net import find_regex_spans


EVAL_PATH = PROJECT_DIR / "data" / "raw" / "korean_eval_300.jsonl"
RESULTS_PATH = PROJECT_DIR / "results" / "results.csv"


def load_jsonl(path: Path) -> list[dict]:
    """Load JSONL rows."""
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def spans_to_char_tags(text: str, spans: list[dict]) -> list[str]:
    """Convert character spans to BIO tags."""
    tags = ["O"] * len(text)

    for span in spans:
        start = span["start"]
        end = span["end"]
        label = span["label"]

        if start >= end or start >= len(text):
            continue

        end = min(end, len(text))
        tags[start] = f"B-{label}"
        for idx in range(start + 1, end):
            tags[idx] = f"I-{label}"

    return tags


def span_objects_to_dicts(spans: list[Span]) -> list[dict]:
    """Convert Span objects to dicts."""
    return [
        {
            "start": span.start,
            "end": span.end,
            "label": span.label,
            "text": span.text,
            "source": span.source,
        }
        for span in spans
    ]


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


def critical_recall(gold_rows: list[dict], pred_rows: list[dict]) -> float:
    """Compute recall for account_number and secret spans."""
    critical_labels = {"account_number", "secret"}

    gold = set()
    pred = set()

    for row in gold_rows:
        for span in row["spans"]:
            if span["label"] in critical_labels:
                gold.add((row["id"], span["start"], span["end"], span["label"]))

    for row in pred_rows:
        for span in row["predicted_spans"]:
            if span["label"] in critical_labels:
                pred.add((row["id"], span["start"], span["end"], span["label"]))

    return len(gold & pred) / len(gold) if gold else 0.0


def false_positive_rate(gold_rows: list[dict], pred_rows: list[dict]) -> float:
    """Compute predicted-span false positive rate."""
    gold = set()
    pred = set()

    for row in gold_rows:
        for span in row["spans"]:
            gold.add((row["id"], span["start"], span["end"], span["label"]))

    for row in pred_rows:
        for span in row["predicted_spans"]:
            pred.add((row["id"], span["start"], span["end"], span["label"]))

    fp = len(pred - gold)
    return fp / len(pred) if pred else 0.0


def run_baseline(redactor: OPF, rows: list[dict]) -> tuple[list[dict], float]:
    """Run OPF-only baseline predictions."""
    pred_rows = []
    start_time = time.perf_counter()

    for idx, row in enumerate(rows, start=1):
        result = redactor.redact(row["text"])
        spans = span_objects_to_dicts(normalize_opf_spans(result))

        pred_rows.append({
            "id": row["id"],
            "domain": row["domain"],
            "text": row["text"],
            "gold_spans": row["spans"],
            "predicted_spans": spans,
        })

        if idx % 50 == 0:
            print(f"[BASELINE] processed {idx}/{len(rows)}")

    elapsed = time.perf_counter() - start_time
    return pred_rows, elapsed


def run_hybrid(redactor: OPF, rows: list[dict]) -> tuple[list[dict], float]:
    """Run OPF plus regex predictions."""
    pred_rows = []
    start_time = time.perf_counter()

    for idx, row in enumerate(rows, start=1):
        result = redactor.redact(row["text"])
        opf_spans = normalize_opf_spans(result)

        regex_spans = [
            Span(
                start=span.start,
                end=span.end,
                label=span.label,
                text=span.text,
                source=span.source,
            )
            for span in find_regex_spans(row["text"])
        ]

        merged = filter_contextual_spans(row["text"], merge_spans(opf_spans + regex_spans))
        spans = span_objects_to_dicts(merged)

        pred_rows.append({
            "id": row["id"],
            "domain": row["domain"],
            "text": row["text"],
            "gold_spans": row["spans"],
            "predicted_spans": spans,
        })

        if idx % 50 == 0:
            print(f"[HYBRID] processed {idx}/{len(rows)}")

    elapsed = time.perf_counter() - start_time
    return pred_rows, elapsed


def compute_metrics(rows: list[dict], pred_rows: list[dict], elapsed: float) -> dict:
    """Compute seqeval, exact span, critical recall, FPR, and latency."""
    y_true = []
    y_pred = []

    for gold_row, pred_row in zip(rows, pred_rows):
        y_true.append(spans_to_char_tags(gold_row["text"], gold_row["spans"]))
        y_pred.append(spans_to_char_tags(gold_row["text"], pred_row["predicted_spans"]))

    exact = exact_span_scores(rows, pred_rows)

    metrics = {
        "rows": len(rows),
        "seqeval_precision": precision_score(y_true, y_pred, zero_division=0),
        "seqeval_recall": recall_score(y_true, y_pred, zero_division=0),
        "seqeval_f1": f1_score(y_true, y_pred, zero_division=0),
        "exact_precision": exact["exact_precision"],
        "exact_recall": exact["exact_recall"],
        "exact_f1": exact["exact_f1"],
        "tp": exact["tp"],
        "fp": exact["fp"],
        "fn": exact["fn"],
        "critical_recall": critical_recall(rows, pred_rows),
        "false_positive_rate": false_positive_rate(rows, pred_rows),
        "total_seconds": elapsed,
        "seconds_per_example": elapsed / len(rows),
        "classification_report": classification_report(y_true, y_pred, zero_division=0),
    }

    return metrics


def append_results(run_name: str, device: str, metrics: dict) -> None:
    """Append one run to results.csv."""
    fieldnames = [
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
        "critical_recall",
        "false_positive_rate",
        "total_seconds",
        "seconds_per_example",
    ]

    write_header = not RESULTS_PATH.exists()

    with RESULTS_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        row = {key: metrics[key] for key in fieldnames if key in metrics}
        row["run_name"] = run_name
        row["device"] = device
        writer.writerow(row)


def save_predictions(run_name: str, pred_rows: list[dict]) -> None:
    """Save predictions as JSONL."""
    path = PROJECT_DIR / "results" / f"{run_name}_predictions.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for row in pred_rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    print(f"[OK] predictions: {path}")


def main() -> None:
    rows = load_jsonl(EVAL_PATH)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[INFO] rows={len(rows)} device={device}")
    redactor = OPF(device=device, output_mode="typed")

    baseline_rows, baseline_time = run_baseline(redactor, rows)
    baseline_metrics = compute_metrics(rows, baseline_rows, baseline_time)
    append_results("baseline_opf_eval300", device, baseline_metrics)
    save_predictions("baseline_opf_eval300", baseline_rows)

    hybrid_rows, hybrid_time = run_hybrid(redactor, rows)
    hybrid_metrics = compute_metrics(rows, hybrid_rows, hybrid_time)
    append_results("hybrid_opf_regex_eval300", device, hybrid_metrics)
    save_predictions("hybrid_opf_regex_eval300", hybrid_rows)

    print("\n[BASELINE]")
    for key, value in baseline_metrics.items():
        if key != "classification_report":
            print(key, value)

    print("\n[HYBRID]")
    for key, value in hybrid_metrics.items():
        if key != "classification_report":
            print(key, value)

    report_path = PROJECT_DIR / "results" / "hybrid_classification_report.txt"
    report_path.write_text(hybrid_metrics["classification_report"], encoding="utf-8")
    print(f"\n[OK] report: {report_path}")


if __name__ == "__main__":
    main()
