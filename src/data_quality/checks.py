"""Funções de verificação de qualidade de dados e agregação em um score.

Cada `check_*` recebe um `pandas.DataFrame` e devolve um score de 0 a 100
(por coluna, ou um único valor). `DataQualityReport` acumula os scores de
várias verificações e calcula uma nota por coluna e uma nota geral.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


def check_completeness(df, columns):
    """Percentual de valores não nulos em cada coluna (0-100)."""
    total = len(df)
    results = {}
    for col in columns:
        if total == 0:
            results[col] = 0.0
            continue
        non_null = df[col].notna().sum()
        results[col] = round(non_null / total * 100, 2)
    return results


def check_uniqueness(df, columns):
    """Percentual de valores únicos (entre os não nulos) em cada coluna (0-100)."""
    results = {}
    for col in columns:
        series = df[col].dropna()
        if len(series) == 0:
            results[col] = 0.0
            continue
        results[col] = round(series.nunique() / len(series) * 100, 2)
    return results


def check_value_range(df, column, min_value, max_value):
    """Percentual de valores (não nulos) dentro de [min_value, max_value] (0-100)."""
    series = df[column].dropna()
    if len(series) == 0:
        return 0.0
    in_range = series.between(min_value, max_value).sum()
    return round(in_range / len(series) * 100, 2)


def check_regex_format(df, column, pattern):
    """Percentual de valores (não nulos) que casam com o regex informado (0-100)."""
    series = df[column].dropna().astype(str)
    if len(series) == 0:
        return 0.0
    regex = re.compile(pattern)
    matches = series.apply(lambda v: regex.match(v) is not None).sum()
    return round(matches / len(series) * 100, 2)


@dataclass
class DataQualityReport:
    """Agrega resultados de checks em um score de 0-100 por coluna e geral.

    Cada coluna pode receber vários scores (ex.: completude + formato) —
    o score da coluna é a média desses scores, e o score geral é a média
    dos scores por coluna.
    """

    scores: dict = field(default_factory=dict)

    def add(self, column: str, score: float) -> None:
        self.scores.setdefault(column, []).append(score)

    def add_completeness(self, df, columns):
        for col, score in check_completeness(df, columns).items():
            self.add(col, score)

    def add_uniqueness(self, df, columns):
        for col, score in check_uniqueness(df, columns).items():
            self.add(col, score)

    def add_value_range(self, df, column, min_value, max_value):
        self.add(column, check_value_range(df, column, min_value, max_value))

    def add_regex_format(self, df, column, pattern):
        self.add(column, check_regex_format(df, column, pattern))

    def column_score(self, column: str) -> float:
        values = self.scores.get(column, [])
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)

    def overall_score(self) -> float:
        if not self.scores:
            return 0.0
        column_scores = [self.column_score(col) for col in self.scores]
        return round(sum(column_scores) / len(column_scores), 2)

    def render(self) -> str:
        lines = ["=== Data Quality Report ===", ""]
        for col in sorted(self.scores):
            lines.append(f"{col:<20} score: {self.column_score(col):6.2f} / 100")
        lines.append("")
        lines.append(f"{'OVERALL':<20} score: {self.overall_score():6.2f} / 100")
        return "\n".join(lines)
