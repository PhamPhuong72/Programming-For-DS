"""Reusable quality-audit and row-count verification helpers (D1 & Section 3.4)."""
from __future__ import annotations

from typing import Sequence
import pandas as pd


def _row_len(obj: pd.DataFrame | int) -> int:
    return obj if isinstance(obj, int) else len(obj)


def report_row_change(
    step: str,
    before: pd.DataFrame | int,
    after: pd.DataFrame | int,
    reason: str,
) -> dict:
    """Report change in row count; caller must provide an explicit justification."""
    if not reason.strip():
        raise ValueError("Explain why the data changed.")
    n_before = _row_len(before)
    n_after = _row_len(after)
    delta = n_after - n_before
    pct = (delta / n_before * 100.0) if n_before > 0 else 0.0
    print(
        f"[AUDIT] {step}: {n_before:,} -> {n_after:,} dòng "
        f"({delta:+,} | {pct:+.2f}%) | Lý do: {reason}"
    )
    return {
        "step": step,
        "before_rows": n_before,
        "after_rows": n_after,
        "delta_rows": delta,
        "delta_pct": round(pct, 4),
        "reason": reason,
    }


def verify_merge(
    step: str,
    left: pd.DataFrame,
    right: pd.DataFrame,
    merged: pd.DataFrame,
    on: str | Sequence[str],
    how: str,
    reason: str,
) -> dict:
    """Verify table merge cardinality, row counts, and unmatched keys (Criterion D1)."""
    if not reason.strip():
        raise ValueError("Provide a reason for the merge.")
    keys = [on] if isinstance(on, str) else list(on)
    left_keys = set(left[keys[0]].dropna()) if len(keys) == 1 else set(map(tuple, left[keys].dropna().to_numpy()))
    right_keys = set(right[keys[0]].dropna()) if len(keys) == 1 else set(map(tuple, right[keys].dropna().to_numpy()))
    unmatched_left = len(left_keys - right_keys)
    unmatched_right = len(right_keys - left_keys)
    delta = len(merged) - len(left)
    print(
        f"[MERGE D1] {step} ({how} on {keys}): "
        f"left={len(left):,}, right={len(right):,} -> merged={len(merged):,} ({delta:+,}) | "
        f"unmatched left keys={unmatched_left:,}, unmatched right keys={unmatched_right:,} | "
        f"Lý do: {reason}"
    )
    return {
        "step": step,
        "how": how,
        "keys": ",".join(keys),
        "left_rows": len(left),
        "right_rows": len(right),
        "merged_rows": len(merged),
        "unmatched_left_keys": unmatched_left,
        "unmatched_right_keys": unmatched_right,
        "reason": reason,
    }


def missing_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Counts and percentages of missing values per column."""
    return (
        pd.DataFrame(
            {
                "missing_count": df.isna().sum(),
                "missing_pct": (df.isna().mean() * 100).round(2),
                "dtype": df.dtypes.astype(str),
            }
        )
        .sort_values(["missing_pct", "missing_count"], ascending=False)
    )
