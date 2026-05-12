
from __future__ import annotations

import random
import string
from datetime import date, timedelta

from faker import Faker


fake = Faker("ko_KR")
random.seed(42)
Faker.seed(42)


def generate_rrn() -> str:
    """Generate a fake Korean resident registration number."""
    birth = fake.date_of_birth(minimum_age=18, maximum_age=75)
    yy = birth.year % 100
    mm = birth.month
    dd = birth.day
    gender_code = random.choice(["1", "2", "3", "4"])
    suffix = "".join(random.choices(string.digits, k=6))
    return f"{yy:02d}{mm:02d}{dd:02d}-{gender_code}{suffix}"


def generate_business_number() -> str:
    """Generate a fake Korean business registration number."""
    return (
        f"{random.randint(100, 999)}-"
        f"{random.randint(10, 99)}-"
        f"{random.randint(10000, 99999)}"
    )


def generate_api_key() -> str:
    """Generate a fake API key-like secret."""
    alphabet = string.ascii_letters + string.digits
    body = "".join(random.choices(alphabet, k=32))
    return f"sk-proj-{body}"


def generate_password() -> str:
    """Generate a fake password-like secret."""
    words = ["Dankook", "Privacy", "Secure", "Project", "Kfilter"]
    symbols = ["!", "#", "@", "$"]
    return f"{random.choice(words)}{random.choice(symbols)}{random.randint(1000, 9999)}"


def generate_phone() -> str:
    """Generate a fake Korean phone number."""
    prefix = random.choice(["010", "02", "031", "032", "051"])
    if prefix == "010":
        return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    return f"{prefix}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def generate_email() -> str:
    """Generate a fake email address."""
    return fake.email()


def generate_name() -> str:
    """Generate a fake Korean person name."""
    return fake.name()


def generate_address() -> str:
    """Generate a fake Korean address."""
    return fake.address().replace("\n", " ")


def generate_date_text() -> str:
    """Generate a fake date string in mixed Korean formats."""
    base = date.today() - timedelta(days=random.randint(0, 3650))
    fmt = random.choice(["dash", "dot", "slash", "korean"])
    if fmt == "dash":
        return base.strftime("%Y-%m-%d")
    if fmt == "dot":
        return base.strftime("%Y.%m.%d")
    if fmt == "slash":
        return base.strftime("%Y/%m/%d")
    return f"{base.year}년 {base.month}월 {base.day}일"


def generate_account_number() -> str:
    """Generate a fake account/card/passport-like identifier."""
    pattern = random.choice(["bank", "card", "passport"])
    if pattern == "bank":
        return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}"
    if pattern == "card":
        return "-".join(str(random.randint(1000, 9999)) for _ in range(4))
    return random.choice(["M", "S", "R"]) + "".join(random.choices(string.digits, k=8))


def generate_by_label(label: str) -> str:
    """Generate one fake PII value for an OPF label."""
    if label == "private_person":
        return generate_name()
    if label == "private_address":
        return generate_address()
    if label == "private_email":
        return generate_email()
    if label == "private_phone":
        return generate_phone()
    if label == "private_url":
        return fake.url()
    if label == "private_date":
        return generate_date_text()
    if label == "account_number":
        return random.choice([generate_rrn(), generate_business_number(), generate_account_number()])
    if label == "secret":
        return random.choice([generate_api_key(), generate_password()])
    raise ValueError(f"unsupported label: {label}")


if __name__ == "__main__":
    labels = [
        "private_person",
        "private_address",
        "private_email",
        "private_phone",
        "private_url",
        "private_date",
        "account_number",
        "secret",
    ]

    for label in labels:
        print(label, "=>", generate_by_label(label))
