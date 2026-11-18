"""Reusable audit, data-loading, statistical, and modeling helpers for the MyAnimeList project."""

from .audit import missing_overview, report_row_change, verify_merge
from .utils import (
    bootstrap_ci,
    extract_franchise_relations,
    find_project_root,
    iter_list_parts,
    load_clean_tables,
    resolve_clean_dataset_dir,
    resolve_raw_dataset_dir,
    setup_plot_style,
)
from .models import (
    build_tabular_preprocessor,
    compute_permutation_importance_df,
)

__all__ = [
    "missing_overview",
    "report_row_change",
    "verify_merge",
    "bootstrap_ci",
    "extract_franchise_relations",
    "find_project_root",
    "iter_list_parts",
    "load_clean_tables",
    "resolve_clean_dataset_dir",
    "resolve_raw_dataset_dir",
    "setup_plot_style",
    "build_tabular_preprocessor",
    "compute_permutation_importance_df",
]
