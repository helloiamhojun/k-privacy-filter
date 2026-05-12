
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

LABELS = {
    "private_person",
    "private_address",
    "private_email",
    "private_phone",
    "private_url",
    "private_date",
    "account_number",
    "secret",
}


def validate_file(path: Path) -> None:
    """Validate JSONL examples with text and character-offset spans."""
    errors = []
    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue

            row = json.loads(line)
            rows.append(row)
            text = row["text"]
            spans = sorted(row["spans"], key=lambda s: (s["start"], s["end"]))

            prev_end = -1
            for span in spans:
                start = span["start"]
                end = span["end"]
                label = span["label"]
                expected = span["text"]
                actual = text[start:end]

                if label not in LABELS:
                    errors.append(f"line {line_no}: bad label {label}")

                if actual != expected:
                    errors.append(
                        f"line {line_no}: offset mismatch id={row.get('id')} "
                        f"expected={expected!r} actual={actual!r}"
                    )

                if start < prev_end:
                    errors.append(f"line {line_no}: overlapping span id={row.get('id')}")

                prev_end = end

    domain_counts = Counter(row.get("domain", "unknown") for row in rows)
    label_counts = Counter(span["label"] for row in rows for span in row["spans"])

    print(f"[OK] rows: {len(rows)}")
    print(f"[OK] domain_counts: {dict(domain_counts)}")
    print(f"[OK] label_counts: {dict(label_counts)}")

    if errors:
        print("\n[ERRORS]")
        for error in errors[:50]:
            print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_jsonl_spans.py /path/to/file.jsonl")

    validate_file(Path(sys.argv[1]))
