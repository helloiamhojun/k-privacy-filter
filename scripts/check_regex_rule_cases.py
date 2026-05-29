from __future__ import annotations

from regex_safety_net import find_regex_spans, mask_text


CASES = [
    {
        "id": "school_account_address",
        "text": "내 아이디는 chjspd이고, 비밀번호는 32215116이고, 내 학번은 32215116이고, 내 집 주소는 경기도 용인시 수지구 1336-2야.",
        "must_mask": ["chjspd", "32215116", "경기도 용인시 수지구 1336-2"],
    },
    {
        "id": "unique_identifiers",
        "text": "주민번호는 900101-1234567, 외국인등록번호는 900101-5234567, 사업자번호는 123-45-67890, 법인등록번호는 110111-1234567입니다.",
        "must_mask": ["900101-1234567", "900101-5234567", "123-45-67890", "110111-1234567"],
    },
    {
        "id": "passport_driver_birth",
        "text": "생년월일은 2001-03-04이고 여권번호는 M12345678이고 운전면허번호는 12 34 567890 12입니다.",
        "must_mask": ["2001-03-04", "M12345678", "12 34 567890 12"],
    },
    {
        "id": "contact_network",
        "text": "전화는 +82-10-1234-5678이고 IP는 192.168.0.15, MAC주소는 AA:BB:CC:DD:EE:FF입니다.",
        "must_mask": ["+82-10-1234-5678", "192.168.0.15", "AA:BB:CC:DD:EE:FF"],
    },
    {
        "id": "finance_auth",
        "text": "계좌는 국민 110-123-456789이고 카드번호는 1234-5678-9012-3456이고 카드 CVC는 123, OTP는 123456입니다.",
        "must_mask": ["국민 110-123-456789", "1234-5678-9012-3456", "123", "123456"],
    },
    {
        "id": "obfuscated_email_location_url",
        "text": "메일은 test.user [at] example.com이고 좌표는 37.56650, 126.97800이고 프로필 url은 example.com/u/hojun입니다.",
        "must_mask": ["test.user [at] example.com", "37.56650, 126.97800", "example.com/u/hojun"],
    },
    {
        "id": "person_context_names",
        "text": "내 이름은 최호준이고 수령자는 박서연 고객님입니다. 보호자 이지은에게 연락해.",
        "must_mask": ["최호준", "박서연", "이지은"],
    },
    {
        "id": "school_person_context",
        "text": "담당 교사는 남궁민수입니다. 학생 오세훈이고 학번은 32215116입니다.",
        "must_mask": ["남궁민수", "오세훈", "32215116"],
    },
]


NEGATIVE_CASES = [
    "모델명은 900101-1234567-A입니다.",
    "문서 버전은 sk-proj-example-not-real로 표시했습니다.",
    "상품코드는 010-1234-5678-A입니다.",
]


def main() -> None:
    failures: list[str] = []

    for case in CASES:
        spans = find_regex_spans(case["text"])
        masked = mask_text(case["text"], spans)
        for value in case["must_mask"]:
            if value in masked:
                failures.append(f"{case['id']}: value was not masked: {value}")

    for text in NEGATIVE_CASES:
        spans = find_regex_spans(text)
        if spans:
            failures.append(f"negative case flagged: {text} -> {spans}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"OK: {len(CASES)} positive cases and {len(NEGATIVE_CASES)} negative cases passed.")


if __name__ == "__main__":
    main()
