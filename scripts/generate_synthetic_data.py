
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

PROJECT_DIR = Path("/content/drive/MyDrive/k-privacy-filter")
SCRIPT_DIR = PROJECT_DIR / "scripts"
sys.path.append(str(SCRIPT_DIR))

from pii_generators import generate_by_label


random.seed(42)

LABELS = [
    "private_person",
    "private_address",
    "private_email",
    "private_phone",
    "private_url",
    "private_date",
    "account_number",
    "secret",
]

TEMPLATES = [
    ("chat", "{private_person}한테 {private_phone}로 연락해줘.", ["private_person", "private_phone"]),
    ("chat", "내 주민번호는 {account_number}인데 저장하지 마.", ["account_number"]),
    ("chat", "{private_person} 주소가 {private_address} 맞아?", ["private_person", "private_address"]),
    ("chat", "임시 비밀번호 {secret}로 로그인하면 돼.", ["secret"]),
    ("chat", "회의 날짜는 {private_date}이고 담당자는 {private_person}야.", ["private_date", "private_person"]),
    ("chat", "이 링크 {private_url}는 개인 페이지니까 공유하지 마.", ["private_url"]),

    ("mail", "안녕하세요 {private_person}님, 답변은 {private_email}로 보내주세요.", ["private_person", "private_email"]),
    ("mail", "배송지는 {private_address}로 등록되어 있습니다.", ["private_address"]),
    ("mail", "본인확인 번호 {account_number}는 확인 후 폐기하겠습니다.", ["account_number"]),
    ("mail", "계약일 {private_date} 기준으로 문서를 작성했습니다.", ["private_date"]),
    ("mail", "문의 연락처는 {private_phone}입니다.", ["private_phone"]),
    ("mail", "첨부파일 암호는 {secret}입니다.", ["secret"]),

    ("memo", "{private_person} 생년월일 {private_date} 확인.", ["private_person", "private_date"]),
    ("memo", "계좌번호 {account_number} 월세 입금용.", ["account_number"]),
    ("memo", "개인 메일 {private_email}로 영수증 받기.", ["private_email"]),
    ("memo", "집 주소 {private_address} 택배 메모에 남김.", ["private_address"]),
    ("memo", "서버 토큰 {secret} 삭제 필요.", ["secret"]),
    ("memo", "공유 링크 {private_url} 비공개 전환.", ["private_url"]),

    ("dev", "로그에 user_email={private_email} 값이 그대로 찍혔다.", ["private_email"]),
    ("dev", "환경변수 API_KEY={secret}는 커밋하면 안 된다.", ["secret"]),
    ("dev", "callback_url={private_url} 파라미터에 사용자 정보가 있다.", ["private_url"]),
    ("dev", "admin_name={private_person}, phone={private_phone} 라인이 남았다.", ["private_person", "private_phone"]),
    ("dev", "billing_account={account_number} 값을 마스킹해야 한다.", ["account_number"]),
    ("dev", "address_field={private_address}가 디버그 로그에 포함됐다.", ["private_address"]),
]


def fill_template(template: str, labels: list[str]) -> tuple[str, list[dict]]:
    """Fill one template and return text with span annotations."""
    values = {}
    for label in labels:
        values[label] = generate_by_label(label)

    text = template.format(**values)
    spans = []

    for label, value in values.items():
        start = text.find(value)
        if start == -1:
            raise ValueError(f"cannot find generated value: {value}")
        spans.append({
            "start": start,
            "end": start + len(value),
            "label": label,
            "text": value,
        })

    spans = sorted(spans, key=lambda s: (s["start"], s["end"]))
    return text, spans


def main() -> None:
    out_path = PROJECT_DIR / "data" / "processed" / "synthetic_train_5000.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for i in range(5000):
        domain, template, labels = random.choice(TEMPLATES)
        text, spans = fill_template(template, labels)

        rows.append({
            "id": f"synthetic_{i + 1:05d}",
            "domain": domain,
            "text": text,
            "spans": spans,
        })

    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"[OK] wrote rows: {len(rows)}")
    print(f"[OK] output: {out_path}")


if __name__ == "__main__":
    main()
