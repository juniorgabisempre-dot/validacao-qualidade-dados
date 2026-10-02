"""Biblioteca leve de validação de qualidade de dados."""

from .checks import (
    DataQualityReport,
    check_completeness,
    check_regex_format,
    check_uniqueness,
    check_value_range,
)

__all__ = [
    "DataQualityReport",
    "check_completeness",
    "check_regex_format",
    "check_uniqueness",
    "check_value_range",
]
