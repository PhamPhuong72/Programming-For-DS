"""Reusable data discovery, memory-safe Parquet streaming, and statistical utilities."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable, Iterator, Sequence
import zipfile

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

NA_SAFE_KWARGS = dict(keep_default_na=False, na_values=[""])

REQUIRED_STEP4_FILES = {
    "manifest.csv",
    "row_count_log.csv",
    "value_cleaning_log.csv",
    "AnimeList_clean.csv",
    "UserList_clean.csv",
}


def find_project_root(start: Path | None = None) -> Path:
    """Locate the repository root from either root or notebooks/ directory."""
    origin = (start or Path.cwd()).resolve()
    for candidate in (origin, *origin.parents):
        if (candidate / "environment.yml").exists() or (candidate / "src" / "audit.py").exists():
            return candidate
    return origin


def _is_valid_step4_dir(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    names = {p.name for p in folder.iterdir()}
    return REQUIRED_STEP4_FILES <= names and (folder / "user_anime_list_parts").is_dir()


def resolve_clean_dataset_dir(root: Path | None = None) -> Path:
    """Locate step4_clean_v1 locally under data/processed/ or on Kaggle (/kaggle/input)."""
    proj = find_project_root(root)
    kaggle_input = Path("/kaggle/input")
    kaggle_working = Path("/kaggle/working")
    preferred_kaggle = Path("/kaggle/input/datasets/chuyenhocielts/myanimelist-clean")

    search_roots = (
        [preferred_kaggle, kaggle_input, kaggle_working]
        if kaggle_input.exists()
        else [proj / "data" / "processed"]
    )
    manifests = sorted(
        {
            m.resolve()
            for base in search_roots
            if base.exists()
            for m in base.rglob("manifest.csv")
            if _is_valid_step4_dir(m.parent)
        }
    )
    if not manifests and kaggle_input.exists():
        archives = list(kaggle_input.rglob("step4_clean_v1.zip"))
        if archives:
            with zipfile.ZipFile(archives[0]) as zf:
                zf.extractall(kaggle_working)
            manifests = sorted(
                {
                    m.resolve()
                    for m in kaggle_working.rglob("manifest.csv")
                    if _is_valid_step4_dir(m.parent)
                }
            )
    if not manifests:
        raise FileNotFoundError(
            "Không tìm thấy bộ dữ liệu sạch step4_clean_v1. "
            "Hãy tải https://www.kaggle.com/datasets/chuyenhocielts/myanimelist-clean "
            "vào data/processed/ hoặc gắn dataset này trên Kaggle."
        )
    return manifests[0].parent


def resolve_raw_dataset_dir(root: Path | None = None) -> Path | None:
    """Return directory containing raw CSVs if available locally or on Kaggle."""
    proj = find_project_root(root)
    candidates = [proj / "data" / "raw", proj / "data", Path("/kaggle/input")]
    for base in candidates:
        if not base.exists():
            continue
        found = {p.name: p.parent for p in base.rglob("*.csv") if p.name in {"AnimeList.csv", "UserList.csv"}}
        if {"AnimeList.csv", "UserList.csv"} <= found.keys():
            return found["AnimeList.csv"]
    return None


def load_clean_tables(
    root: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, list[Path], dict[str, pd.DataFrame]]:
    """Load AnimeList_clean, UserList_clean, sorted Parquet part paths, and audit logs."""
    clean_dir = resolve_clean_dataset_dir(root)
    anime = pd.read_csv(clean_dir / "AnimeList_clean.csv", **NA_SAFE_KWARGS)
    users = pd.read_csv(clean_dir / "UserList_clean.csv", **NA_SAFE_KWARGS)
    parts = sorted((clean_dir / "user_anime_list_parts").glob("*.parquet"))
    if not parts:
        raise FileNotFoundError(f"Không có file Parquet trong {clean_dir / 'user_anime_list_parts'}")
    logs = {
        "manifest": pd.read_csv(clean_dir / "manifest.csv"),
        "row_log": pd.read_csv(clean_dir / "row_count_log.csv"),
        "value_log": pd.read_csv(clean_dir / "value_cleaning_log.csv"),
    }
    return anime, users, parts, logs


def iter_list_parts(
    parts: Sequence[Path],
    columns: Sequence[str] | None = None,
) -> Iterator[tuple[int, pd.DataFrame]]:
    """Stream cleaned UserAnimeList Parquet parts one by one with column projection."""
    cols = list(columns) if columns is not None else None
    for idx, path in enumerate(parts, start=1):
        yield idx, pd.read_parquet(path, columns=cols)


def bootstrap_ci(
    values: Sequence[float] | pd.Series | np.ndarray,
    stat_fn: Callable[[np.ndarray], float] = np.mean,
    n_boot: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Compute point estimate and percentile bootstrap confidence interval (Criterion D5)."""
    arr = pd.Series(values).dropna().to_numpy(dtype=float)
    if len(arr) == 0:
        return np.nan, np.nan, np.nan
    point = float(stat_fn(arr))
    if len(arr) == 1:
        return point, point, point
    rng = np.random.default_rng(seed)
    n = len(arr)
    # Vectorized bootstrap in batches to bound peak RAM on large arrays
    batch_size = min(200, n_boot)
    stats_list: list[np.ndarray] = []
    remaining = n_boot
    while remaining > 0:
        b = min(batch_size, remaining)
        idx = rng.integers(0, n, size=(b, n))
        samples = arr[idx]
        if stat_fn is np.mean:
            boot_vals = samples.mean(axis=1)
        elif stat_fn is np.median:
            boot_vals = np.median(samples, axis=1)
        else:
            boot_vals = np.apply_along_axis(stat_fn, 1, samples)
        stats_list.append(boot_vals)
        remaining -= b
    all_boot = np.concatenate(stats_list)
    alpha = (1.0 - ci) / 2.0
    low, high = np.quantile(all_boot, [alpha, 1.0 - alpha])
    return point, float(low), float(high)


def extract_franchise_relations(anime_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse `related` dictionary strings into anime-level franchise roles and Prequel->Sequel edges."""
    valid_ids = set(anime_df["anime_id"].astype(int))
    roles: list[dict] = []
    edges: list[dict] = []

    for row in anime_df[["anime_id", "related"]].itertuples(index=False):
        aid = int(row.anime_id)
        raw = row.related
        parsed = None
        if pd.notna(raw) and str(raw).strip() not in {"", "[]"}:
            try:
                parsed = ast.literal_eval(str(raw))
            except (ValueError, SyntaxError):
                parsed = None

        if not isinstance(parsed, dict) or not parsed:
            roles.append(
                {
                    "anime_id": aid,
                    "has_prequel": False,
                    "has_sequel": False,
                    "n_anime_relations": 0,
                    "franchise_role": "Standalone",
                }
            )
            continue

        prequel_ids: list[int] = []
        sequel_ids: list[int] = []
        anime_rel_count = 0

        for rel_type, items in parsed.items():
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict) or item.get("type") != "anime":
                    continue
                target_id = item.get("mal_id")
                if target_id is None:
                    continue
                target_id = int(target_id)
                anime_rel_count += 1
                if rel_type == "Prequel":
                    prequel_ids.append(target_id)
                    if target_id in valid_ids:
                        edges.append({"prequel_id": target_id, "sequel_id": aid})
                elif rel_type == "Sequel":
                    sequel_ids.append(target_id)

        has_pre = len(prequel_ids) > 0
        has_seq = len(sequel_ids) > 0
        if has_pre:
            role = "Direct Sequel"
        elif has_seq:
            role = "Franchise Root"
        elif anime_rel_count > 0:
            role = "Side Story / Spin-off"
        else:
            role = "Standalone"

        roles.append(
            {
                "anime_id": aid,
                "has_prequel": has_pre,
                "has_sequel": has_seq,
                "n_anime_relations": anime_rel_count,
                "franchise_role": role,
            }
        )

    roles_df = pd.DataFrame(roles)
    edges_df = pd.DataFrame(edges).drop_duplicates().reset_index(drop=True)
    return roles_df, edges_df


def setup_plot_style() -> None:
    """Configure consistent Matplotlib & Seaborn styling with full Vietnamese Unicode support."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial", "Liberation Sans"],
            "axes.unicode_minus": False,
            "figure.dpi": 120,
            "savefig.dpi": 150,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
            "legend.fontsize": 9.5,
        }
    )
