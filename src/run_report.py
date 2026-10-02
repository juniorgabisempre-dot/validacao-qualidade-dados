"""Carrega o CSV sintético, roda os checks de qualidade e imprime um relatório
formatado com o score por coluna e o score geral.

Uso:
    python src/generate_sample_data.py   # gera data/customers_orders.csv
    python src/run_report.py             # roda os checks e imprime o relatório
"""
from pathlib import Path

import pandas as pd

from data_quality import DataQualityReport

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "customers_orders.csv"
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def main():
    if not DATA_PATH.exists():
        raise SystemExit(
            f"Arquivo não encontrado: {DATA_PATH}\n"
            "Rode antes: python src/generate_sample_data.py"
        )

    df = pd.read_csv(DATA_PATH)

    report = DataQualityReport()
    report.add_completeness(
        df, ["customer_id", "customer_name", "email", "order_amount", "order_date"]
    )
    report.add_uniqueness(df, ["customer_id", "order_id"])
    report.add_value_range(df, "order_amount", 0, 5000)
    report.add_regex_format(df, "email", EMAIL_PATTERN)

    print(f"Linhas avaliadas: {len(df)}\n")
    print(report.render())


if __name__ == "__main__":
    main()
