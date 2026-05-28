from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from regex_safety_net import find_regex_spans, is_contextual_false_positive


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_DIR / "results" / "final_kpf_experiments"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def normalize_span(span: Any) -> dict[str, Any]:
    if isinstance(span, dict):
        return {
            "start": int(span["start"]),
            "end": int(span["end"]),
            "label": str(span["label"]),
            "text": str(span["text"]),
            "source": str(span.get("source", "unknown")),
        }
    return {
        "start": int(span.start),
        "end": int(span.end),
        "label": str(span.label),
        "text": str(span.text),
        "source": str(getattr(span, "source", "regex")),
    }


def merge_span_dicts(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_spans = sorted(
        spans,
        key=lambda s: (s["start"], 0 if s.get("source") == "regex" else 1, -(s["end"] - s["start"])),
    )
    kept: list[dict[str, Any]] = []

    for span in sorted_spans:
        if not any(span["start"] < existing["end"] and span["end"] > existing["start"] for existing in kept):
            kept.append(span)

    return sorted(kept, key=lambda s: (s["start"], s["end"]))


def final_kpf_from_existing(text: str, existing_spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filtered_existing = [
        normalize_span(span)
        for span in existing_spans
        if not is_contextual_false_positive(
            text,
            int(span["start"]),
            int(span["end"]),
            str(span["label"]),
            str(span["text"]),
        )
    ]
    enhanced_regex = [normalize_span(span) for span in find_regex_spans(text)]
    return merge_span_dicts(filtered_existing + enhanced_regex)


def exact_match(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    return (
        gold["label"] == pred["label"]
        and gold["start"] == pred["start"]
        and gold["end"] == pred["end"]
    )


def covered(gold: dict[str, Any], pred: dict[str, Any]) -> bool:
    return (
        gold["label"] == pred["label"]
        and pred["start"] <= gold["start"]
        and pred["end"] >= gold["end"]
    )


def span_scores(gold_rows: list[dict[str, Any]], pred_rows: list[dict[str, Any]]) -> dict[str, Any]:
    gold_set = set()
    pred_set = set()
    covered_hits = 0
    label_gold = Counter()
    label_exact = Counter()
    label_covered = Counter()

    pred_by_id = {row["id"]: row for row in pred_rows}

    for row in gold_rows:
        pred_spans = pred_by_id[row["id"]]["predicted_spans"]
        for span in row["spans"]:
            key = (row["id"], span["start"], span["end"], span["label"])
            gold_set.add(key)
            label_gold[span["label"]] += 1
            if any(exact_match(span, pred) for pred in pred_spans):
                label_exact[span["label"]] += 1
            if any(covered(span, pred) for pred in pred_spans):
                covered_hits += 1
                label_covered[span["label"]] += 1

    for row in pred_rows:
        for span in row["predicted_spans"]:
            pred_set.add((row["id"], span["start"], span["end"], span["label"]))

    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "covered_recall": covered_hits / len(gold_set) if gold_set else 0.0,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "label_exact_recall": {label: label_exact[label] / count for label, count in label_gold.items()},
        "label_covered_recall": {label: label_covered[label] / count for label, count in label_gold.items()},
    }


def hard_negative_scores(rows: list[dict[str, Any]]) -> dict[str, Any]:
    flagged = [row for row in rows if row["predicted_spans"]]
    return {
        "rows": len(rows),
        "flagged": len(flagged),
        "fpr": len(flagged) / len(rows) if rows else 0.0,
        "examples": flagged[:10],
    }


def update_prediction_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    updated = []
    for row in rows:
        old_spans = row.get("predicted_spans", [])
        new_spans = final_kpf_from_existing(row["text"], old_spans)
        new_row = dict(row)
        new_row["previous_predicted_spans"] = old_spans
        new_row["predicted_spans"] = new_spans
        updated.append(new_row)
    return updated


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Final KPF Offline Experiments",
        "",
        "Existing OPF/Hybrid predictions were reused, then the final regex expansion and contextual false-positive suppression were applied.",
        "",
        "## Main Eval 300",
        "",
        "| System | Precision | Recall | F1 | Covered Recall | FP | FN |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for system in ["existing_hybrid", "final_kpf"]:
        s = summary["eval300"][system]
        lines.append(
            f"| {system} | {s['precision']:.4f} | {s['recall']:.4f} | {s['f1']:.4f} | {s['covered_recall']:.4f} | {s['fp']} | {s['fn']} |"
        )

    lines.extend([
        "",
        "## Hard Negative 100",
        "",
        "| System | Flagged | FPR |",
        "|---|---:|---:|",
    ])
    for system in ["existing_hybrid", "final_kpf"]:
        s = summary["hard_negative"][system]
        lines.append(f"| {system} | {s['flagged']}/{s['rows']} | {s['fpr']:.4f} |")

    lines.extend([
        "",
        "## Adversarial 10",
        "",
        "| System | Precision | Recall | F1 | Covered Recall | FP | FN |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for system in ["existing_hybrid", "final_kpf"]:
        s = summary["adversarial"][system]
        lines.append(
            f"| {system} | {s['precision']:.4f} | {s['recall']:.4f} | {s['f1']:.4f} | {s['covered_recall']:.4f} | {s['fp']} | {s['fn']} |"
        )

    lines.extend(["", "## Remaining Hard-Negative False Positives", ""])
    examples = summary["hard_negative"]["final_kpf"]["examples"]
    if not examples:
        lines.append("- None in the sampled hard-negative set.")
    for row in examples:
        pred = ", ".join(f"{span['label']}={span['text']}" for span in row["predicted_spans"])
        lines.append(f"- `{row['id']}` {row['text']} -> {pred}")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    eval_gold = load_jsonl(PROJECT_DIR / "data" / "raw" / "korean_eval_300.jsonl")
    eval_existing = load_jsonl(PROJECT_DIR / "results" / "hybrid_opf_regex_eval300_predictions.jsonl")
    eval_existing_normalized = [
        {
            "id": row["id"],
            "text": row["text"],
            "spans": row["gold_spans"],
            "predicted_spans": row["predicted_spans"],
        }
        for row in eval_existing
    ]
    eval_final = update_prediction_rows(eval_existing_normalized)

    hard_existing = load_jsonl(PROJECT_DIR / "results" / "extra_eval" / "hybrid_hard_negative_predictions.jsonl")
    hard_existing_normalized = [
        {"id": row["id"], "text": row["text"], "spans": row.get("gold_spans", []), "predicted_spans": row["predicted_spans"]}
        for row in hard_existing
    ]
    hard_final = update_prediction_rows(hard_existing_normalized)

    adversarial_gold = load_jsonl(PROJECT_DIR / "results" / "extra_eval" / "adversarial_eval.jsonl")
    adversarial_existing = load_jsonl(PROJECT_DIR / "results" / "extra_eval" / "hybrid_adversarial_predictions.jsonl")
    adversarial_existing_normalized = [
        {
            "id": row["id"],
            "text": row["text"],
            "spans": row.get("gold_spans", []),
            "predicted_spans": row["predicted_spans"],
        }
        for row in adversarial_existing
    ]
    adversarial_final = update_prediction_rows(adversarial_existing_normalized)

    summary = {
        "eval300": {
            "existing_hybrid": span_scores(eval_gold, eval_existing_normalized),
            "final_kpf": span_scores(eval_gold, eval_final),
        },
        "hard_negative": {
            "existing_hybrid": hard_negative_scores(hard_existing_normalized),
            "final_kpf": hard_negative_scores(hard_final),
        },
        "adversarial": {
            "existing_hybrid": span_scores(adversarial_gold, adversarial_existing_normalized),
            "final_kpf": span_scores(adversarial_gold, adversarial_final),
        },
    }

    write_jsonl(OUT_DIR / "eval300_final_predictions.jsonl", eval_final)
    write_jsonl(OUT_DIR / "hard_negative_final_predictions.jsonl", hard_final)
    write_jsonl(OUT_DIR / "adversarial_final_predictions.jsonl", adversarial_final)
    (OUT_DIR / "final_kpf_offline_scores.json").write_text(
        json.dumps(summary, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "final_kpf_offline_report.md").write_text(render_report(summary), encoding="utf-8")

    print(render_report(summary))


if __name__ == "__main__":
    main()
