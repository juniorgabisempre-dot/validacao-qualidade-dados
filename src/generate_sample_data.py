"""Gera um CSV sintético de clientes/pedidos (dados fake via Faker) com
problemas de qualidade injetados de propósito, para os checks terem algo
real a pegar.

Uso:
    python src/generate_sample_data.py
"""
import csv
import random
from pathlib import Path

from faker import Faker

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "customers_orders.csv"
ROW_COUNT = 500
BAD_ROW_RATIO = 0.08  # ~8% das linhas recebem um problema

FIELDNAMES = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "order_id",
    "order_amount",
    "order_date",
]


def generate_rows(n=ROW_COUNT, seed=42):
    fake = Faker("pt_BR")
    Faker.seed(seed)
    random.seed(seed)

    rows = []
    for i in range(1, n + 1):
        rows.append(
            {
                "customer_id": i,
                "customer_name": fake.name(),
                "email": fake.email(),
                "country": fake.country(),
                "order_id": 1000 + i,
                "order_amount": round(random.uniform(10, 2000), 2),
                "order_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
            }
        )

    bad_count = int(n * BAD_ROW_RATIO)
    bad_indexes = random.sample(range(n), bad_count)
    for idx in bad_indexes:
        problem = random.choice(["null_email", "null_amount", "bad_email", "duplicate_id"])
        if problem == "null_email":
            rows[idx]["email"] = ""
        elif problem == "null_amount":
            rows[idx]["order_amount"] = ""
        elif problem == "bad_email":
            rows[idx]["email"] = "nao-e-um-email"
        elif problem == "duplicate_id":
            candidates = [j for j in range(n) if j != idx]
            other = rows[random.choice(candidates)]
            rows[idx]["customer_id"] = other["customer_id"]

    return rows


def main():
    rows = generate_rows()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gerado: {OUTPUT_PATH} ({len(rows)} linhas)")


if __name__ == "__main__":
    main()
