"""Testes de sanidade (assert-based, sem framework) para data_quality.checks.

Uso:
    python -m tests.test_checks
    (ou, de dentro da pasta tests: python test_checks.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pandas as pd  # noqa: E402

from data_quality.checks import (  # noqa: E402
    DataQualityReport,
    check_completeness,
    check_regex_format,
    check_uniqueness,
    check_value_range,
)


def test_check_completeness():
    df = pd.DataFrame({"a": [1, 2, None, 4], "b": [1, None, None, None]})
    result = check_completeness(df, ["a", "b"])
    assert result["a"] == 75.0, result
    assert result["b"] == 25.0, result


def test_check_completeness_empty_df():
    df = pd.DataFrame({"a": []})
    assert check_completeness(df, ["a"])["a"] == 0.0


def test_check_uniqueness():
    df = pd.DataFrame({"a": [1, 1, 2, 3], "b": [1, 2, 3, 4]})
    result = check_uniqueness(df, ["a", "b"])
    assert result["a"] == 75.0, result
    assert result["b"] == 100.0, result


def test_check_value_range():
    df = pd.DataFrame({"a": [1, 5, 10, 15]})
    result = check_value_range(df, "a", 0, 10)
    assert result == 75.0, result


def test_check_regex_format():
    df = pd.DataFrame({"email": ["a@b.com", "not-an-email", "c@d.org", None]})
    result = check_regex_format(df, "email", r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    assert result == 66.67, result  # 2 de 3 valores não nulos casam com o padrão


def test_data_quality_report_aggregates_scores():
    df = pd.DataFrame({"a": [1, 2, None, 4]})
    report = DataQualityReport()
    report.add_completeness(df, ["a"])
    assert report.column_score("a") == 75.0
    assert report.overall_score() == 75.0


def test_data_quality_report_averages_multiple_checks_per_column():
    df = pd.DataFrame({"a": [1, 2, 3, 4]})  # 100% completo, 100% único
    report = DataQualityReport()
    report.add_completeness(df, ["a"])
    report.add_uniqueness(df, ["a"])
    report.add_value_range(df, "a", 0, 2)  # só 2 de 4 valores no range -> 50%
    assert report.column_score("a") == round((100 + 100 + 50) / 3, 2)


def run_all():
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"OK: {t.__name__}")
    print(f"\n{len(tests)} testes passaram.")


if __name__ == "__main__":
    run_all()
