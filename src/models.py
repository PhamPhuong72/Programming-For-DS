"""Reusable scikit-learn Pipeline builders and model interpretation utilities."""
from __future__ import annotations

from typing import Sequence
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_tabular_preprocessor(
    numeric_cols: Sequence[str],
    categorical_cols: Sequence[str],
    min_category_freq: int | float | None = None,
    scale_numeric: bool = True,
) -> ColumnTransformer:
    """Construct a leakage-free ColumnTransformer for numeric and categorical features."""
    num_steps: list[tuple[str, object]] = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))
    num_pipe = Pipeline(num_steps)

    ohe_kwargs: dict = {"handle_unknown": "ignore", "sparse_output": False}
    if min_category_freq is not None:
        ohe_kwargs["min_frequency"] = min_category_freq
    cat_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
            ("onehot", OneHotEncoder(**ohe_kwargs)),
        ]
    )

    transformers = []
    if numeric_cols:
        transformers.append(("num", num_pipe, list(numeric_cols)))
    if categorical_cols:
        transformers.append(("cat", cat_pipe, list(categorical_cols)))
    return ColumnTransformer(transformers=transformers, remainder="drop")


def compute_permutation_importance_df(
    fitted_pipeline: Pipeline,
    X_eval: pd.DataFrame,
    y_eval: pd.Series | np.ndarray,
    scoring: str,
    n_repeats: int = 8,
    random_state: int = 42,
    max_samples: int | None = 15_000,
) -> pd.DataFrame:
    """Compute feature-level permutation importance on held-out test data."""
    if max_samples is not None and len(X_eval) > max_samples:
        rng = np.random.default_rng(random_state)
        idx = rng.choice(len(X_eval), size=max_samples, replace=False)
        X_sub = X_eval.iloc[idx]
        y_sub = pd.Series(y_eval).iloc[idx] if isinstance(y_eval, pd.Series) else y_eval[idx]
    else:
        X_sub, y_sub = X_eval, y_eval

    perm = permutation_importance(
        fitted_pipeline,
        X_sub,
        y_sub,
        scoring=scoring,
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=-1,
    )
    return (
        pd.DataFrame(
            {
                "feature": list(X_eval.columns),
                "importance_mean": perm.importances_mean,
                "importance_std": perm.importances_std,
            }
        )
        .sort_values("importance_mean", ascending=False)
        .reset_index(drop=True)
    )
