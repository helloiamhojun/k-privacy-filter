
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def convert_file(src_path: Path, dst_path: Path) -> None:
    """Convert internal span-list JSONL to OPF span-mapping JSONL."""
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    with src_path.open("r", encoding="utf-8") as src, dst_path.open("w", encoding="utf-8") as dst:
        count = 0

        for line in src:
            if not line.strip():
                continue

            row = json.loads(line)
            span_map = defaultdict(list)

            for span in row["spans"]:
                span_map[span["label"]].append([span["start"], span["end"]])

            opf_row = {
                "text": row["text"],
                "spans": dict(span_map),
            }

            dst.write(json.dumps(opf_row, ensure_ascii=False) + "\n")
            count += 1

    print(f"[OK] converted rows: {count}")
    print(f"[OK] output: {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: convert_to_opf_format.py SRC_JSONL DST_JSONL")

    convert_file(Path(sys.argv[1]), Path(sys.argv[2]))
