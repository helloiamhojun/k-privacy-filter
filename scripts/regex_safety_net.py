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


KOREAN_DIGITS = "\uacf5|\uc601|\uc77c|\uc774|\uc0bc|\uc0ac|\uc624|\uc721|\ub959|\uce60|\ud314|\uad6c"
KOREAN_REGION = (
    r"서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|"
    r"경기도|강원도|충청북도|충청남도|전라북도|전라남도|경상북도|경상남도|제주특별자치도|"
    r"서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주"
)
ADDRESS_TAIL = r"(?:\s*\d{1,4}동)?(?:\s*\d{1,4}호)?(?:\s*(?:\([^)]+\)|[가-힣0-9]{1,20}(?:아파트|빌라|오피스텔|타워|빌딩)))?"


PATTERNS: list[tuple[str, str]] = [
    ("account_number", r"(?<!\d)\d{6}-[1-4]\d{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}\s*[-./]\s*[1-4]\d{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}\s*[-./]\s*[5-8]\d{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}[1-4]\d{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}[5-8]\d{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}-[1-4]\*{6}(?!\d)"),
    ("account_number", r"(?<!\d)\d{3}-\d{2}-\d{5}(?!\d)"),
    ("account_number", r"(?<!\d)\d{3}\s*[-.\s]\s*\d{2}\s*[-.\s]\s*\d{5}(?!\d)"),
    ("account_number", r"(?<!\d)\d{6}-\d{7}(?!\d)"),
    ("account_number", r"(?<!\d)\d{2}-\d{2}-\d{6}-\d{2}(?!\d)"),
    ("account_number", r"(?<!\d)(?:\d{4}[-\s]){3}\d{4}(?!\d)"),
    ("account_number", r"(?<![A-Za-z0-9])[A-Z][0-9]{8}(?![A-Za-z0-9])"),
    ("account_number", r"(?<!\d)\d{10}(?!\d)"),
    ("private_phone", r"(?<!\d)01[016789]-\d{3,4}-\d{4}(?!\d)"),
    ("private_phone", r"(?<!\d)01[016789]\s*[-.\s]\s*\d{3,4}\s*[-.\s]\s*\d{4}(?!\d)"),
    ("private_phone", r"(?<!\d)01[016789]\d{7,8}(?!\d)"),
    ("private_phone", r"(?<!\d)01[016789]\s*[-.\s]\s*\*{3,4}\s*[-.\s]\s*\d{4}(?!\d)"),
    ("private_phone", r"(?<!\d)0\d{1,2}-\d{3,4}-\d{4}(?!\d)"),
    ("private_phone", r"(?<!\d)0\d{1,2}\s*[-.\s]\s*\d{3,4}\s*[-.\s]\s*\d{4}(?!\d)"),
    (
        "private_phone",
        rf"(?<![\uac00-\ud7a3])(?:{KOREAN_DIGITS}){{2,3}}\s*[-\s]\s*"
        rf"(?:{KOREAN_DIGITS}){{3,4}}\s*[-\s]\s*(?:{KOREAN_DIGITS}){{4}}(?![\uac00-\ud7a3])",
    ),
    (
        "private_address",
        rf"(?:{KOREAN_REGION})\s+"
        r"(?:[가-힣]{1,12}(?:시|군|구)\s+){0,3}"
        r"[가-힣0-9]{1,24}(?:대로|로|길|거리|가)\s*"
        r"\d{1,5}(?:-\d{1,5})?"
        rf"{ADDRESS_TAIL}",
    ),
    (
        "private_address",
        rf"(?:{KOREAN_REGION})\s+"
        r"(?:[가-힣]{1,12}(?:시|군|구)\s+){1,3}"
        r"[가-힣0-9]{1,24}(?:읍|면|동|리)\s*"
        r"\d{1,5}(?:-\d{1,5})?"
        rf"{ADDRESS_TAIL}",
    ),
    ("private_email", r"(?<![A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}(?![A-Za-z0-9._%+\-])"),
    ("private_email", r"(?<![A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]+\s*\[\s*at\s*\]\s*[A-Za-z0-9.\-]+\.[A-Za-z]{2,}(?![A-Za-z0-9._%+\-])"),
    ("private_url", r"https?://[^\s]+"),
    ("secret", r"sk-proj-[A-Za-z0-9_\-]{16,}"),
    ("secret", r"sk-proj-[A-Za-z0-9_\-]*(?:\s+[A-Za-z0-9_\-]+)+"),
    ("secret", r"sk-[A-Za-z0-9_\-]{16,}"),
    ("secret", r"sk_(?:live|test)_[A-Za-z0-9_\-]{12,}"),
    ("secret", r"AKIA[0-9A-Z]{16}"),
    ("secret", r"xox[baprs]-[A-Za-z0-9\-]{10,}"),
    ("secret", r"[A-Z_]*(API_KEY|TOKEN|SECRET|PASSWORD)[A-Z_]*\s*=\s*[A-Za-z0-9_!@#$%^&*.\-]+"),
    ("secret", r"(?<![A-Za-z0-9])(?=[A-Za-z0-9!@#$%^&*]*[!@#$%^&*])(?=[A-Za-z0-9!@#$%^&*]*\d)[A-Za-z][A-Za-z0-9!@#$%^&*]{7,}(?![A-Za-z0-9])"),
]


CONTEXT_VALUE_PATTERNS: list[tuple[str, str]] = [
    (
        "account_number",
        r"(?i)(?:아이디|id|user_id|userid|login_id|계정|계정명)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>[A-Za-z][A-Za-z0-9._-]{2,31})(?![A-Za-z0-9._-])",
    ),
    (
        "private_person",
        r"(?:이름|성명|성함|고객명|회원명|환자명|예금주|담당자|수신자|보낸 사람)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>[가-힣]{2,4}?)(?:님|씨)?(?=이고|이며|입니다|이에요|예요|라고|,|\.|\s|$)",
    ),
    (
        "secret",
        r"(?i)(?:비밀번호|패스워드|password|passwd|pwd|암호)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>[A-Za-z0-9_!@#$%^&*.\-]{6,})(?![A-Za-z0-9_!@#$%^&*.\-])",
    ),
    (
        "account_number",
        r"(?:학번|학생번호|사번|직원번호|회원번호|고객번호)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>\d{5,12})(?!\d)",
    ),
    (
        "private_address",
        rf"(?:주소|배송지|거주지|집 주소|자택 주소|address|address_field)\s*(?:은|는|:|=)?\s*"
        rf"(?P<value>(?:{KOREAN_REGION})\s+"
        r"(?:[가-힣]{1,12}(?:시|군|구)\s+){0,3}"
        r"[가-힣0-9]{1,24}(?:대로|로|길|거리|가)\s*\d{1,5}(?:-\d{1,5})?"
        rf"{ADDRESS_TAIL})",
    ),
    (
        "private_address",
        rf"(?:주소|배송지|거주지|집 주소|자택 주소|address|address_field)\s*(?:은|는|:|=)?\s*"
        rf"(?P<value>(?:{KOREAN_REGION})\s+"
        r"(?:[가-힣]{1,12}(?:시|군|구)\s+){1,3}"
        r"(?:[가-힣0-9]{1,24}(?:읍|면|동|리)\s*)?"
        r"\d{1,5}(?:-\d{1,5})?"
        rf"{ADDRESS_TAIL})(?=야|이야|입니다|이에요|예요|,|\.|\s|$)",
    ),
    (
        "account_number",
        r"(?:계좌번호|계좌)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>\d{2,6}(?:[-\s]\d{2,6}){1,4})(?!\d)",
    ),
    (
        "account_number",
        r"(?:카드번호|신용카드)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>(?:\d{4}[-\s]?){3}\d{4})(?!\d)",
    ),
    (
        "account_number",
        r"(?:여권번호|여권)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>[A-Z][0-9]{8})(?![A-Za-z0-9])",
    ),
    (
        "account_number",
        r"(?:운전면허번호|면허번호|운전면허)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>\d{2}-\d{2}-\d{6}-\d{2})(?!\d)",
    ),
    (
        "account_number",
        r"(?:차량번호|자동차번호|차번호)\s*(?:은|는|:|=)?\s*"
        r"(?P<value>\d{2,3}[가-힣]\s?\d{4})(?!\d)",
    ),
]


NEGATIVE_CONTEXT_MARKERS = [
    "\uac1c\uc778\uc815\ubcf4\uac00 \uc544\ub2d9\ub2c8\ub2e4",
    "\uc2e4\uc81c \ud0a4\uac00 \uc544\ub2d9\ub2c8\ub2e4",
    "\uc2e4\uc81c \uc8fc\ubbfc\ubc88\ud638\uac00 \uc544\ub2d9\ub2c8\ub2e4",
    "\uc5f0\ub77d\ucc98\uac00 \uc544\ub2d9\ub2c8\ub2e4",
    "\uc0ac\uc6a9 \ubd88\uac00\ub2a5",
    "\ub354\ubbf8",
    "\uc0d8\ud50c",
    "\uc608\uc2dc",
    "fixture",
    "placeholder",
    "mock",
    "\ubb38\uc11c \ubc84\uc804",
    "\ubaa8\ub378\uba85",
    "\uc8fc\ubb38\ubc88\ud638",
    "\uc0c1\ud488\ucf54\ub4dc",
    "\uc0c1\ud488 \uc635\uc158 \ucf54\ub4dc",
    "\ub9b4\ub9ac\uc988 \ucf54\ub4dc",
    "\uc7ac\uace0 \uad00\ub9ac \ucf54\ub4dc",
    "\uc2e4\uc81c \uc0ac\uc6a9\uc790\uac00 \uc544\ub2d9\ub2c8\ub2e4",
    "demo",
]


DUMMY_VALUE_MARKERS = [
    "example",
    "dummy",
    "not-real",
    "not_real",
    "sample",
    "demo",
    "fixture",
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

    for label, pattern in CONTEXT_VALUE_PATTERNS:
        for match in re.finditer(pattern, text):
            value = match.group("value")
            start = match.start("value")
            end = match.end("value")
            spans.append(
                RegexSpan(
                    start=start,
                    end=end,
                    label=label,
                    text=value,
                )
            )

    return filter_contextual_false_positives(text, merge_overlapping_spans(spans))


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


def is_contextual_false_positive(
    text: str,
    start: int,
    end: int,
    label: str,
    span_text: str,
) -> bool:
    """Return True for PII-shaped values that local context marks as dummy/test data."""
    window_start = max(0, start - 24)
    window_end = min(len(text), end + 24)
    context = text[window_start:window_end].lower()
    value = span_text.lower()
    suffix = text[end : min(len(text), end + 16)].lower()

    if any(marker.lower() in context for marker in NEGATIVE_CONTEXT_MARKERS):
        return True

    if label == "account_number" and suffix.startswith("-test"):
        return True

    if label == "private_email" and value.endswith(".invalid"):
        return True

    if label in {"account_number", "secret", "private_phone", "private_address"}:
        if any(marker in value for marker in DUMMY_VALUE_MARKERS):
            return True

    return False


def filter_contextual_false_positives(text: str, spans: list[RegexSpan]) -> list[RegexSpan]:
    """Suppress deterministic spans when nearby words identify them as examples/dummies."""
    return [
        span
        for span in spans
        if not is_contextual_false_positive(text, span.start, span.end, span.label, span.text)
    ]


def mask_text(text: str, spans: list[RegexSpan]) -> str:
    """Replace spans with typed placeholders."""
    masked = text

    for span in sorted(spans, key=lambda s: s.start, reverse=True):
        placeholder = f"<{span.label.upper()}>"
        masked = masked[: span.start] + placeholder + masked[span.end :]

    return masked


if __name__ == "__main__":
    examples = [
        "\uae40\ubbfc\uc218 \uc8fc\ubbfc\ubc88\ud638\ub294 900101-1234567\uc774\uace0 \uc804\ud654\ub294 010-1234-5678\uc785\ub2c8\ub2e4.",
        "\uc0ac\uc5c5\uc790\ubc88\ud638 123-45-67890, \uc774\uba54\uc77c test.user@example.com",
        "API_KEY=sk-proj-AbCdEf1234567890abcdef \ud1a0\ud070 \uc81c\uac70",
        "\ube44\ubc00\ubc88\ud638\ub294 Dankook!2026\uc73c\ub85c \uc124\uc815\ud588\uc2b5\ub2c8\ub2e4.",
    ]

    for text in examples:
        spans = find_regex_spans(text)
        print(text)
        print(spans)
        print(mask_text(text, spans))
        print()
