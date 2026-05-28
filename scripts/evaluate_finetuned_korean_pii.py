from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


def load_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if limit is not None and len(rows) >= limit:
                break
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_spans(row: dict[str, Any]) -> list[dict[str, Any]]:
    spans = []
    for span in row.get("spans", row.get("gold_spans", [])):
        spans.append(
            {
                "start": int(span["start"]),
                "end": int(span["end"]),
                "label": str(span["label"]),
                "text": str(span.get("text", row["text"][int(span["start"]) : int(span["end"])])),
            }
        )
    return spans


def predict_spans(model, tokenizer, text: str, device: torch.device, max_length: int) -> list[dict[str, Any]]:
    encoding = tokenizer(
        text,
        return_offsets_mapping=True,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
    )
    offsets = encoding.pop("offset_mapping")[0].tolist()
    encoding = {key: value.to(device) for key, value in encoding.items()}

    with torch.no_grad():
        pred_ids = model(**encoding).logits.argmax(-1)[0].detach().cpu().tolist()

    spans: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for label_id, (start, end) in zip(pred_ids, offsets):
        label = model.config.id2label[int(label_id)]
        if start == end or label == "O":
            if current is not None:
                spans.append(current)
                current = None
            continue

        if "-" not in label:
            if current is not None:
                spans.append(current)
                current = None
            continue

        prefix, entity = label.split("-", 1)
        if prefix == "B" or current is None or current["label"] != entity:
            if current is not None:
                spans.append(current)
            current = {"start": int(start), "end": int(end), "label": entity, "text": text[int(start) : int(end)]}
        else:
            current["end"] = int(end)
            current["text"] = text[int(current["start"]) : int(end)]

    if current is not None:
        spans.append(current)

    return spans


def exact_match(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    return gold["label"] == pred["label"] and gold["start"] == pred["start"] and gold["end"] == pred["end"]


def covered_match(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    return gold["label"] == pred["label"] and pred["start"] <= gold["start"] and pred["end"] >= gold["end"]


def overlap_match(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    return gold["label"] == pred["label"] and pred["start"] < gold["end"] and pred["end"] > gold["start"]


def score_rows(gold_rows: list[dict[str, Any]], pred_rows: list[dict[str, Any]]) -> dict[str, Any]:
    gold_set = set()
    pred_set = set()
    gold_spans_by_id = {}
    pred_spans_by_id = {}
    label_gold = Counter()
    label_exact = Counter()
    label_covered = Counter()
    label_overlap = Counter()

    for row in gold_rows:
        spans = normalize_spans(row)
        gold_spans_by_id[row["id"]] = spans
        for span in spans:
            gold_set.add((row["id"], span["start"], span["end"], span["label"]))
            label_gold[span["label"]] += 1

    for row in pred_rows:
        pred_spans_by_id[row["id"]] = row["predicted_spans"]
        for span in row["predicted_spans"]:
            pred_set.add((row["id"], span["start"], span["end"], span["label"]))

    for row_id, gold_spans in gold_spans_by_id.items():
        pred_spans = pred_spans_by_id.get(row_id, [])
        for gold in gold_spans:
            if any(exact_match(gold, pred) for pred in pred_spans):
                label_exact[gold["label"]] += 1
            if any(covered_match(gold, pred) for pred in pred_spans):
                label_covered[gold["label"]] += 1
            if any(overlap_match(gold, pred) for pred in pred_spans):
                label_overlap[gold["label"]] += 1

    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    covered_hits = sum(label_covered.values())
    overlap_hits = sum(label_overlap.values())
    gold_count = len(gold_set)
    pred_count = len(pred_set)
    flagged_empty_rows = sum(
        1
        for row in pred_rows
        if not gold_spans_by_id.get(row["id"], []) and row["predicted_spans"]
    )
    empty_rows = sum(1 for row in gold_rows if not normalize_spans(row))

    return {
        "rows": len(gold_rows),
        "gold_spans": gold_count,
        "predicted_spans": pred_count,
        "exact_precision": precision,
        "exact_recall": recall,
        "exact_f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "covered_recall": covered_hits / gold_count if gold_count else 0.0,
        "overlap_recall": overlap_hits / gold_count if gold_count else 0.0,
        "empty_rows": empty_rows,
        "flagged_empty_rows": flagged_empty_rows,
        "empty_row_fpr": flagged_empty_rows / empty_rows if empty_rows else 0.0,
        "label_exact_recall": {label: label_exact[label] / count for label, count in label_gold.items()},
        "label_covered_recall": {label: label_covered[label] / count for label, count in label_gold.items()},
        "label_overlap_recall": {label: label_overlap[label] / count for label, count in label_gold.items()},
    }


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Fine-tuned Korean PII Model Evaluation",
        "",
        f"- Model: `{summary['model_dir']}`",
        f"- Device: `{summary['device']}`",
        "",
        "| Dataset | Rows | Exact P | Exact R | Exact F1 | Covered R | Overlap R | Empty-row FPR | FP | FN |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, result in summary["datasets"].items():
        s = result["scores"]
        lines.append(
            f"| {name} | {s['rows']} | {s['exact_precision']:.4f} | {s['exact_recall']:.4f} | {s['exact_f1']:.4f} | "
            f"{s['covered_recall']:.4f} | {s['overlap_recall']:.4f} | {s['empty_row_fpr']:.4f} | {s['fp']} | {s['fn']} |"
        )

    lines.extend(["", "## Notes", ""])
    lines.append("- Exact scores require identical start/end offsets and label.")
    lines.append("- Covered recall counts a gold span as found when the predicted span fully contains it.")
    lines.append("- Overlap recall counts a gold span as found when the predicted span overlaps it with the same label.")
    lines.append("- Synthetic-test scores measure the generated data distribution, not real-world generalization.")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--dataset", action="append", nargs=2, metavar=("NAME", "PATH"), required=True)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    device = torch.device(args.device if args.device == "cpu" or torch.cuda.is_available() else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(args.model_dir)
    model.to(device)
    model.eval()

    summary: dict[str, Any] = {"model_dir": args.model_dir, "device": str(device), "datasets": {}}

    for name, path_text in args.dataset:
        rows = load_jsonl(Path(path_text), args.limit)
        predictions = []
        start_time = time.perf_counter()

        for idx, row in enumerate(rows, start=1):
            pred_spans = predict_spans(model, tokenizer, row["text"], device, args.max_length)
            predictions.append(
                {
                    "id": row["id"],
                    "text": row["text"],
                    "gold_spans": normalize_spans(row),
                    "predicted_spans": pred_spans,
                }
            )
            if idx % 500 == 0:
                print(f"[{name}] processed {idx}/{len(rows)}")

        elapsed = time.perf_counter() - start_time
        scores = score_rows(rows, predictions)
        scores["total_seconds"] = elapsed
        scores["seconds_per_example"] = elapsed / len(rows) if rows else 0.0
        summary["datasets"][name] = {"path": path_text, "scores": scores}
        write_jsonl(out_dir / f"{name}_predictions.jsonl", predictions)
        print(f"[OK] {name}: {json.dumps(scores, ensure_ascii=False)}")

    (out_dir / "finetuned_eval_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "finetuned_eval_report.md").write_text(render_report(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[OK] wrote evaluation to {out_dir}")


if __name__ == "__main__":
    main()
