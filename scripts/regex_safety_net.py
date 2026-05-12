
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RegexSpan:
    start: int
    end: int
    label: str
    text: str
    source: str = "regex"


PATTERNS: list[tuple[str, str]] = [
    ("account_number", r"(?<!\d)\d{6}-[1-4]\d{6}(?!\d)"),             # Korean RRN
    ("account_number", r"(?<!\d)\d{3}-\d{2}-\d{5}(?!\d)"),            # Korean business number
    ("private_phone", r"(?<!\d)01[016789]-\d{3,4}-\d{4}(?!\d)"),      # mobile
    ("private_phone", r"(?<!\d)0\d{1,2}-\d{3,4}-\d{4}(?!\d)"),        # landline
    ("private_email", r"(?<![A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}(?![A-Za-z0-9._%+\-])"),
    ("private_url", r"https?://[^\s]+"),
    ("secret", r"sk-proj-[A-Za-z0-9_\-]{16,}"),
    ("secret", r"xox[baprs]-[A-Za-z0-9\-]{10,}"),
    ("secret", r"[A-Z_]*(API_KEY|TOKEN|SECRET|PASSWORD)[A-Z_]*\s*=\s*[^\s,;]+"),
    ("secret", r"(?<![A-Za-z0-9])(?=[A-Za-z0-9!@#$%^&*]*[!@#$%^&*])(?=[A-Za-z0-9!@#$%^&*]*\d)[A-Za-z][A-Za-z0-9!@#$%^&*]{7,}(?![A-Za-z0-9])"),
]


def find_regex_spans(text: str) -> list[RegexSpan]:
    """Find deterministic Korean PII and secret spans with regex."""
    spans: list[RegexSpan] = []

    for label, pattern in PATTERNS:
        for match in re.finditer(pattern, text):
            spans.append(
                RegexSpan(
                    start=match.start(),
                    end=match.end(),
                    label=label,
                    text=match.group(0),
                )
            )

    return merge_overlapping_spans(spans)


def merge_overlapping_spans(spans: list[RegexSpan]) -> list[RegexSpan]:
    """Keep the longest span when regex matches overlap."""
    sorted_spans = sorted(spans, key=lambda s: (s.start, -(s.end - s.start)))
    kept: list[RegexSpan] = []

    for span in sorted_spans:
        overlaps = False
        for existing in kept:
            if span.start < existing.end and span.end > existing.start:
                overlaps = True
                break

        if not overlaps:
            kept.append(span)

    return sorted(kept, key=lambda s: (s.start, s.end))


def mask_text(text: str, spans: list[RegexSpan]) -> str:
    """Replace spans with typed placeholders."""
    masked = text

    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        placeholder = f"<{span.label.upper()}>"
        masked = masked[:span.start] + placeholder + masked[span.end:]

    return masked


if __name__ == "__main__":
    examples = [
        "김민수 주민번호는 900101-1234567이고 전화는 010-1234-5678입니다.",
        "사업자번호 123-45-67890, 이메일 test.user@example.com",
        "API_KEY=sk-proj-AbCdEf1234567890abcdef 토큰 삭제",
        "비밀번호는 Dankook!2026으로 설정했습니다.",
    ]

    for text in examples:
        spans = find_regex_spans(text)
        print(text)
        print(spans)
        print(mask_text(text, spans))
        print()
