"""Small reusable quality-audit helpers. No dataset-specific analysis."""
from __future__ import annotations
import pandas as pd


def report_row_change(step: str, before: pd.DataFrame, after: pd.DataFrame, reason: str) -> None:
    """Report change in row count; caller must provide an actual reason."""
    if not reason.strip():
        raise ValueError("Explain why the data changed.")
    delta = len(after) - len(before)
    print(f"{step}: {len(before):,} -> {len(after):,} rows ({delta:+,}); reason: {reason}")


def missing_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Counts and percentages only; you must interpret missingness."""
    return pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(2),
    }).sort_values("missing_pct", ascending=False)
