
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from opf import OPF

PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
SCRIPT_DIR = PROJECT_DIR / "scripts"
sys.path.append(str(SCRIPT_DIR))

from regex_safety_net import find_regex_spans


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    label: str
    text: str
    source: str


def normalize_opf_spans(result) -> list[Span]:
    """Convert OPF detected spans to local Span objects."""
    spans: list[Span] = []

    for span in result.detected_spans:
        spans.append(
            Span(
                start=int(span.start),
                end=int(span.end),
                label=str(span.label),
                text=str(span.text),
                source="opf",
            )
        )

    return spans


def trim_span_boundary(span: Span) -> Span:
    """Trim common Korean sentence endings from over-wide address spans."""
    if span.label != "private_address":
        return span

    trim_suffixes = [
        "입니다.",
        "입니다",
        "맞아?",
        "맞아",
        "인가요?",
        "인가요",
        "입니다?",
    ]

    text = span.text
    end = span.end

    for suffix in trim_suffixes:
        if text.endswith(suffix):
            text = text[: -len(suffix)].rstrip()
            end = span.start + len(text)
            break

    return Span(
        start=span.start,
        end=end,
        label=span.label,
        text=text,
        source=span.source,
    )


def merge_spans(spans: list[Span]) -> list[Span]:
    """Merge OPF and regex spans, preferring longer and regex spans on overlap."""
    spans = [trim_span_boundary(span) for span in spans]

    sorted_spans = sorted(
        spans,
        key=lambda s: (s.start, -(s.end - s.start), 0 if s.source == "regex" else 1),
    )

    kept: list[Span] = []

    for span in sorted_spans:
        has_overlap = False

        for existing in kept:
            if span.start < existing.end and span.end > existing.start:
                has_overlap = True
                break

        if not has_overlap:
            kept.append(span)

    return sorted(kept, key=lambda s: (s.start, s.end))


def mask_text(text: str, spans: list[Span]) -> str:
    """Replace detected spans with typed placeholders."""
    masked = text

    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        masked = masked[:span.start] + f"<{span.label.upper()}>" + masked[span.end:]

    return masked


class KPrivacyPipeline:
    """Hybrid OPF + Korean regex privacy filter."""

    def __init__(self, device: str = "cuda") -> None:
        self.redactor = OPF(device=device, output_mode="typed")

    def detect(self, text: str) -> list[Span]:
        """Detect PII spans from OPF and regex safety net."""
        opf_result = self.redactor.redact(text)
        opf_spans = normalize_opf_spans(opf_result)

        regex_spans = [
            Span(
                start=span.start,
                end=span.end,
                label=span.label,
                text=span.text,
                source=span.source,
            )
            for span in find_regex_spans(text)
        ]

        print(f"[STAGE-1] OPF detected {len(opf_spans)} spans")
        print(f"[STAGE-3] regex detected {len(regex_spans)} spans")

        return merge_spans(opf_spans + regex_spans)

    def redact(self, text: str) -> dict:
        """Return masked text and detected spans."""
        spans = self.detect(text)
        masked = mask_text(text, spans)

        return {
            "text": text,
            "masked_text": masked,
            "spans": [span.__dict__ for span in spans],
        }


if __name__ == "__main__":
    pipe = KPrivacyPipeline(device="cuda")

    examples = [
        "김민수 주민번호는 900101-1234567이고 전화는 010-1234-5678입니다.",
        "API_KEY=sk-proj-AbCdEf1234567890abcdef 토큰 삭제하고 박서연에게 메일 보내.",
        "Alice Smith was born on 1990-01-02. Her email is alice@example.com.",
    ]

    for text in examples:
        result = pipe.redact(text)
        print("\nINPUT:", result["text"])
        print("MASKED:", result["masked_text"])
        print("SPANS:", result["spans"])
