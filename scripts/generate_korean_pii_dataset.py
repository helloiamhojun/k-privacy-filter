from __future__ import annotations

import argparse
import json
import random
import string
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Callable


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

SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황"]
GIVEN = [
    "민수",
    "서연",
    "지훈",
    "하은",
    "도윤",
    "예린",
    "현우",
    "수빈",
    "지민",
    "유진",
    "준호",
    "채원",
    "성민",
    "나연",
    "태현",
    "소희",
]
REGIONS = [
    "서울특별시",
    "부산광역시",
    "대구광역시",
    "인천광역시",
    "광주광역시",
    "대전광역시",
    "울산광역시",
    "세종특별자치시",
    "경기도",
    "강원특별자치도",
    "충청북도",
    "충청남도",
    "전북특별자치도",
    "전라남도",
    "경상북도",
    "경상남도",
    "제주특별자치도",
]
CITIES = ["강남구", "마포구", "송파구", "해운대구", "수성구", "화성시", "성남시", "수원시", "청주시", "전주시", "창원시", "제주시"]
ROADS = ["테헤란로", "동탄역로", "중앙로", "서부로", "대학로", "세종대로", "해맞이길", "은행로", "산업단지로", "혁신로"]
EMAIL_IDS = ["minsu", "seoyeon", "jinho", "privacy.user", "kfilter.test", "student01", "office.admin", "customer.help"]
DOMAINS = ["example.com", "testmail.co.kr", "sample.net", "school.ac.kr", "company.co.kr"]
BANKS = ["국민", "신한", "하나", "우리", "농협", "카카오뱅크"]
ORDER_WORDS = ["주문번호", "예약번호", "접수번호", "쿠폰번호", "상품코드", "모델명", "송장번호"]


def digits(n: int) -> str:
    return "".join(random.choices(string.digits, k=n))


def token(n: int, alphabet: str = string.ascii_letters + string.digits) -> str:
    return "".join(random.choices(alphabet, k=n))


def gen_name() -> str:
    if random.random() < 0.15:
        return random.choice(["홍길동", "김철수", "이영희"])
    return random.choice(SURNAMES) + random.choice(GIVEN)


def gen_address() -> str:
    region = random.choice(REGIONS)
    city = random.choice(CITIES)
    road = random.choice(ROADS)
    main_no = random.randint(1, 220)
    detail = random.choice(
        [
            f"{random.randint(1, 120)}동 {random.randint(101, 2405)}호",
            f"{random.randint(2, 18)}층 {random.randint(1, 30)}호",
            f"{random.randint(101, 999)}호",
            f"{random.randint(1, 80)}번지",
            f"{random.randint(1, 12)}차 아파트 {random.randint(101, 1505)}호",
        ]
    )
    return f"{region} {city} {road} {main_no} {detail}"


def gen_email() -> str:
    suffix = random.choice(["", str(random.randint(1, 999)), "_" + digits(2)])
    return f"{random.choice(EMAIL_IDS)}{suffix}@{random.choice(DOMAINS)}"


def gen_phone() -> str:
    kind = random.choice(["mobile_dash", "mobile_plain", "landline", "spoken"])
    if kind == "mobile_dash":
        return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    if kind == "mobile_plain":
        return f"010{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    if kind == "landline":
        area = random.choice(["02", "031", "032", "042", "051", "053", "062", "064"])
        return f"{area}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    return f"공일공-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"


def gen_url() -> str:
    host = random.choice(["profile", "share", "pay", "secure", "docs", "admin"])
    domain = random.choice(["example.com", "sample.co.kr", "test-service.kr", "privacy-lab.dev"])
    return f"https://{host}.{domain}/{token(8).lower()}"


def gen_date_text() -> str:
    base = date.today() - timedelta(days=random.randint(0, 3650))
    fmt = random.choice(["dash", "dot", "slash", "korean", "short_korean"])
    if fmt == "dash":
        return base.strftime("%Y-%m-%d")
    if fmt == "dot":
        return base.strftime("%Y.%m.%d")
    if fmt == "slash":
        return base.strftime("%Y/%m/%d")
    if fmt == "short_korean":
        return f"{base.year % 100:02d}년 {base.month}월 {base.day}일"
    return f"{base.year}년 {base.month}월 {base.day}일"


def gen_rrn() -> str:
    yy = random.randint(50, 99) if random.random() < 0.45 else random.randint(0, 9)
    gender = random.choice(["1", "2", "3", "4", "5", "6", "7", "8"])
    return f"{yy:02d}{random.randint(1, 12):02d}{random.randint(1, 28):02d}-{gender}{digits(6)}"


def gen_business_number() -> str:
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10000, 99999)}"


def gen_corporate_number() -> str:
    return f"{random.randint(100000, 999999)}-{random.randint(1000000, 9999999)}"


def gen_card_number() -> str:
    return "-".join(digits(4) for _ in range(4))


def gen_bank_account() -> str:
    return f"{random.choice(BANKS)} {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}"


def gen_passport() -> str:
    return random.choice(["M", "S", "R"]) + digits(8)


def gen_driver_license() -> str:
    return f"{random.randint(11, 28)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}-{random.randint(10, 99)}"


def gen_vehicle_number() -> str:
    return f"{random.randint(10, 399)}{random.choice(['가', '나', '다', '라', '마', '버', '서', '아', '자'])}{random.randint(1000, 9999)}"


def gen_account_number() -> str:
    return random.choice(
        [
            gen_rrn,
            gen_business_number,
            gen_corporate_number,
            gen_card_number,
            gen_bank_account,
            gen_passport,
            gen_driver_license,
            gen_vehicle_number,
        ]
    )()


def gen_secret() -> str:
    kind = random.choice(["openai", "aws", "slack", "password", "assignment", "jwtish"])
    if kind == "openai":
        return random.choice(["sk-proj-", "sk-"]) + token(random.randint(32, 48))
    if kind == "aws":
        return "AKIA" + token(16, string.ascii_uppercase + string.digits)
    if kind == "slack":
        return random.choice(["xoxb-", "xoxp-"]) + digits(11) + "-" + digits(12) + "-" + token(24)
    if kind == "assignment":
        return random.choice(["API_KEY=", "SECRET_KEY=", "token="]) + token(28)
    if kind == "jwtish":
        return "eyJ" + token(24) + "." + token(18) + "." + token(24)
    return random.choice(["Privacy", "Dankook", "Secure", "Kfilter", "Chjsp"]) + token(2) + str(random.randint(1000, 9999)) + random.choice(["!", "!@", "#", "$%"])


GENERATOR: dict[str, Callable[[], str]] = {
    "private_person": gen_name,
    "private_address": gen_address,
    "private_email": gen_email,
    "private_phone": gen_phone,
    "private_url": gen_url,
    "private_date": gen_date_text,
    "account_number": gen_account_number,
    "secret": gen_secret,
}

TEMPLATES: list[tuple[str, list[str]]] = [
    ("chat", ["내 이름은 ", "private_person", "이고 전화번호는 ", "private_phone", "야. 주소는 ", "private_address", "로 보내줘."]),
    ("chat", ["아이디는 ", "account_number", "이고 비밀번호는 ", "secret", "이야."]),
    ("chat", ["성함 ", "private_person", ", 생년월일 ", "private_date", ", 연락처 ", "private_phone", " 확인 부탁해."]),
    ("commerce", ["배송지는 ", "private_address", "이고 수령자는 ", "private_person", "입니다. 주문자 메일은 ", "private_email", "입니다."]),
    ("commerce", ["카드번호 ", "account_number", "로 결제했고 영수증 링크는 ", "private_url", "입니다."]),
    ("finance", ["예금주 ", "private_person", " 계좌번호 ", "account_number", " 입금 확인해 주세요."]),
    ("finance", ["본인확인 번호는 ", "account_number", "이고 휴대폰은 ", "private_phone", "입니다."]),
    ("dev", ["로그에 user_email=", "private_email", ", API_KEY=", "secret", ", callback=", "private_url", " 값이 남았습니다."]),
    ("dev", ["관리자 이름=", "private_person", " phone=", "private_phone", " token=", "secret", " 제거 필요."]),
    ("school", ["학생 ", "private_person", "의 보호자 연락처는 ", "private_phone", "이고 주소는 ", "private_address", "입니다."]),
    ("health", ["환자명 ", "private_person", ", 예약일 ", "private_date", ", 연락처 ", "private_phone", ", 메모 비밀번호 ", "secret", "."]),
    ("gov", ["주민/외국인등록번호 ", "account_number", "는 민원 서류에서 마스킹해야 합니다."]),
    ("gov", ["사업자 또는 법인 번호 ", "account_number", "와 담당자 ", "private_person", " 이메일 ", "private_email", "."]),
    ("mobility", ["운전면허/차량 식별값 ", "account_number", "와 기사 연락처 ", "private_phone", "가 포함됨."]),
    ("mixed", ["주소:", "private_address", " 이름:", "private_person", " api 키:", "secret", " 메일:", "private_email"]),
    ("mixed", ["여권번호는 ", "account_number", "이고 여행자명은 ", "private_person", ", 출국일은 ", "private_date", "입니다."]),
]

HARD_NEGATIVE_TEMPLATES = [
    "주문번호 {code}는 배송 조회용이라 개인정보가 아닙니다.",
    "상품코드 {code}와 모델명 {model}은 제품 식별자입니다.",
    "예시 전화번호 010-0000-0000은 더미 데이터입니다.",
    "샘플 이메일 test@example.com은 문서 예제입니다.",
    "API 문서의 placeholder sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 는 실제 키가 아닙니다.",
    "버전 v{major}.{minor}.{patch} 배포 완료, 담당 팀은 보안실입니다.",
    "좌석번호 A-{seat}와 접수번호 R-{code}는 행사 운영 코드입니다.",
    "테스트 주소 서울특별시 중구 세종대로 0은 실제 거주지가 아닙니다.",
]


def build_positive(example_id: str) -> dict:
    domain, parts = random.choice(TEMPLATES)
    text_parts: list[str] = []
    spans: list[dict] = []

    for part in parts:
        if part in GENERATOR:
            value = GENERATOR[part]()
            start = sum(len(x) for x in text_parts)
            text_parts.append(value)
            spans.append({"start": start, "end": start + len(value), "label": part, "text": value})
        else:
            text_parts.append(part)

    return {"id": example_id, "domain": domain, "text": "".join(text_parts), "spans": spans}


def build_hard_negative(example_id: str) -> dict:
    template = random.choice(HARD_NEGATIVE_TEMPLATES)
    text = template.format(
        code=random.choice([digits(8), f"{digits(4)}-{digits(4)}", token(10).upper()]),
        model=random.choice(["KF-2026-A1", "PRIVACY-X200", "DKU-SAFE-11"]),
        major=random.randint(1, 4),
        minor=random.randint(0, 12),
        patch=random.randint(0, 20),
        seat=random.randint(1, 80),
    )
    return {"id": example_id, "domain": "hard_negative", "text": text, "spans": []}


def validate_rows(rows: list[dict]) -> None:
    errors: list[str] = []
    for row in rows:
        prev_end = -1
        for span in sorted(row["spans"], key=lambda item: (item["start"], item["end"])):
            actual = row["text"][span["start"] : span["end"]]
            if actual != span["text"]:
                errors.append(f"{row['id']}: expected={span['text']!r} actual={actual!r}")
            if span["start"] < prev_end:
                errors.append(f"{row['id']}: overlapping spans")
            prev_end = span["end"]
    if errors:
        raise ValueError("\n".join(errors[:20]))


def make_split(split: str, size: int, hard_negative_ratio: float) -> list[dict]:
    rows = []
    for idx in range(size):
        example_id = f"korean_pii_{split}_{idx + 1:06d}"
        if random.random() < hard_negative_ratio:
            rows.append(build_hard_negative(example_id))
        else:
            rows.append(build_positive(example_id))
    validate_rows(rows)
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize(rows: list[dict]) -> dict:
    return {
        "rows": len(rows),
        "domains": dict(Counter(row["domain"] for row in rows)),
        "labels": dict(Counter(span["label"] for row in rows for span in row["spans"])),
        "empty_span_rows": sum(1 for row in rows if not row["spans"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="data/processed/korean_pii_large")
    parser.add_argument("--train-size", type=int, default=50000)
    parser.add_argument("--val-size", type=int, default=5000)
    parser.add_argument("--test-size", type=int, default=5000)
    parser.add_argument("--hard-negative-ratio", type=float, default=0.18)
    parser.add_argument("--seed", type=int, default=20260529)
    args = parser.parse_args()

    random.seed(args.seed)
    out_dir = Path(args.out_dir)
    splits = {
        "train": make_split("train", args.train_size, args.hard_negative_ratio),
        "val": make_split("val", args.val_size, args.hard_negative_ratio),
        "test": make_split("test", args.test_size, args.hard_negative_ratio),
    }

    summary = {"seed": args.seed, "labels": LABELS, "splits": {}}
    for split, rows in splits.items():
        write_jsonl(out_dir / f"{split}.jsonl", rows)
        summary["splits"][split] = summarize(rows)

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[OK] wrote dataset to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
