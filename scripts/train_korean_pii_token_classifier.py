from __future__ import annotations

import argparse
import inspect
import json
import os
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)


PII_LABELS = [
    "private_person",
    "private_address",
    "private_email",
    "private_phone",
    "private_url",
    "private_date",
    "account_number",
    "secret",
]

BIO_LABELS = ["O"] + [f"{prefix}-{label}" for label in PII_LABELS for prefix in ("B", "I")]
LABEL2ID = {label: idx for idx, label in enumerate(BIO_LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}


def load_rows(path: Path, limit: int | None = None) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if limit is not None and len(rows) >= limit:
                break
    return rows


def labels_for_offsets(offsets: list[tuple[int, int]], spans: list[dict]) -> list[int]:
    labels = [-100] * len(offsets)
    span_tokens: dict[int, list[int]] = {idx: [] for idx in range(len(spans))}

    for token_idx, (start, end) in enumerate(offsets):
        if start == end:
            continue
        labels[token_idx] = LABEL2ID["O"]
        for span_idx, span in enumerate(spans):
            if start < span["end"] and end > span["start"]:
                span_tokens[span_idx].append(token_idx)
                break

    for span_idx, token_indices in span_tokens.items():
        if not token_indices:
            continue
        label = spans[span_idx]["label"]
        if label not in PII_LABELS:
            raise ValueError(f"unsupported label: {label}")
        labels[token_indices[0]] = LABEL2ID[f"B-{label}"]
        for token_idx in token_indices[1:]:
            labels[token_idx] = LABEL2ID[f"I-{label}"]

    return labels


class KoreanPiiDataset(Dataset):
    def __init__(self, rows: list[dict], tokenizer, max_length: int) -> None:
        self.rows = rows
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, idx: int) -> dict:
        row = self.rows[idx]
        encoding = self.tokenizer(
            row["text"],
            truncation=True,
            max_length=self.max_length,
            return_offsets_mapping=True,
        )
        offsets = encoding.pop("offset_mapping")
        encoding["labels"] = labels_for_offsets(offsets, row.get("spans", []))
        return encoding


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    pred_ids = np.argmax(predictions, axis=-1)

    total = 0
    correct = 0
    true_sequences: list[list[str]] = []
    pred_sequences: list[list[str]] = []

    for pred_row, label_row in zip(pred_ids, labels):
        true_seq: list[str] = []
        pred_seq: list[str] = []
        for pred_id, label_id in zip(pred_row, label_row):
            if label_id == -100:
                continue
            total += 1
            correct += int(pred_id == label_id)
            true_seq.append(ID2LABEL[int(label_id)])
            pred_seq.append(ID2LABEL[int(pred_id)])
        true_sequences.append(true_seq)
        pred_sequences.append(pred_seq)

    metrics = {"token_accuracy": correct / total if total else 0.0}
    try:
        from seqeval.metrics import f1_score, precision_score, recall_score

        metrics.update(
            {
                "entity_precision": float(precision_score(true_sequences, pred_sequences)),
                "entity_recall": float(recall_score(true_sequences, pred_sequences)),
                "entity_f1": float(f1_score(true_sequences, pred_sequences)),
            }
        )
    except Exception as exc:
        metrics["seqeval_error"] = str(exc)[:180]
    return metrics


def training_arguments(args) -> TrainingArguments:
    kwargs = {
        "output_dir": str(args.output_dir),
        "num_train_epochs": args.epochs,
        "per_device_train_batch_size": args.train_batch_size,
        "per_device_eval_batch_size": args.eval_batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "learning_rate": args.learning_rate,
        "weight_decay": args.weight_decay,
        "logging_steps": args.logging_steps,
        "save_steps": args.save_steps,
        "save_total_limit": 2,
        "report_to": "none",
        "fp16": bool(torch.cuda.is_available() and args.fp16),
        "dataloader_num_workers": 0,
    }

    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" in signature.parameters:
        kwargs["eval_strategy"] = "steps"
    else:
        kwargs["evaluation_strategy"] = "steps"
    if "save_safetensors" in signature.parameters:
        kwargs["save_safetensors"] = True

    supported_kwargs = {key: value for key, value in kwargs.items() if key in signature.parameters}
    dropped_kwargs = sorted(set(kwargs) - set(supported_kwargs))
    if dropped_kwargs:
        print(f"[WARN] dropped unsupported TrainingArguments: {dropped_kwargs}")

    return TrainingArguments(**supported_kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-jsonl", required=True)
    parser.add_argument("--val-jsonl", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-name", default="distilbert-base-multilingual-cased")
    parser.add_argument("--max-train-examples", type=int, default=12000)
    parser.add_argument("--max-val-examples", type=int, default=1500)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--train-batch-size", type=int, default=16)
    parser.add_argument("--eval-batch-size", type=int, default=32)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=3e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--logging-steps", type=int, default=50)
    parser.add_argument("--save-steps", type=int, default=300)
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args()

    os.environ.setdefault("WANDB_DISABLED", "true")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    args.output_dir = Path(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] torch={torch.__version__} cuda={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)}")
    print(f"[INFO] model={args.model_name}")

    train_rows = load_rows(Path(args.train_jsonl), args.max_train_examples)
    val_rows = load_rows(Path(args.val_jsonl), args.max_val_examples)
    print(f"[INFO] train_rows={len(train_rows)} val_rows={len(val_rows)}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(
        args.model_name,
        num_labels=len(BIO_LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    train_dataset = KoreanPiiDataset(train_rows, tokenizer, args.max_length)
    val_dataset = KoreanPiiDataset(val_rows, tokenizer, args.max_length)
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    trainer_kwargs = {
        "model": model,
        "args": training_arguments(args),
        "train_dataset": train_dataset,
        "eval_dataset": val_dataset,
        "data_collator": data_collator,
        "compute_metrics": compute_metrics,
    }
    trainer_signature = inspect.signature(Trainer.__init__)
    if "tokenizer" in trainer_signature.parameters:
        trainer_kwargs["tokenizer"] = tokenizer
    elif "processing_class" in trainer_signature.parameters:
        trainer_kwargs["processing_class"] = tokenizer

    trainer = Trainer(**trainer_kwargs)

    start = time.time()
    train_output = trainer.train()
    train_seconds = time.time() - start
    eval_metrics = trainer.evaluate()

    final_dir = args.output_dir / "final"
    trainer.save_model(str(final_dir))
    tokenizer.save_pretrained(str(final_dir))

    saved_weight = None
    for name in ["model.safetensors", "pytorch_model.bin"]:
        if (final_dir / name).exists():
            saved_weight = name
            break
    if saved_weight is None:
        raise SystemExit(f"[ERROR] no model weight file saved in {final_dir}")

    result = {
        "model_name": args.model_name,
        "train_rows": len(train_rows),
        "val_rows": len(val_rows),
        "labels": BIO_LABELS,
        "train_runtime_seconds": train_seconds,
        "train_metrics": train_output.metrics,
        "eval_metrics": eval_metrics,
        "final_dir": str(final_dir),
        "saved_weight": saved_weight,
    }
    result_path = args.output_dir / "training_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] saved model to {final_dir}")
    print(f"[OK] saved weight file: {saved_weight}")


if __name__ == "__main__":
    main()
