from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = Path("data") / "output" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _plot_category_counts(df: pd.DataFrame) -> Path | None:
    if "category" not in df.columns:
        return None
    counts = df["category"].value_counts().sort_values(ascending=False)
    if counts.empty:
        return None
    plt.figure(figsize=(8, 4))
    counts.plot(kind="bar", color="#4F6BED")
    plt.title("Events by Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "events_by_category.png"
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def _plot_category_conversion(df: pd.DataFrame) -> Path | None:
    if "category" not in df.columns or "activity" not in df.columns:
        return None
    try:
        conv = df.groupby("category")["activity"].mean().sort_values(ascending=False)
    except Exception:
        return None
    if conv.empty:
        return None
    plt.figure(figsize=(8, 4))
    (conv * 100).plot(kind="bar", color="#F6AD55")
    plt.title("Activity Rate by Category (%)")
    plt.xlabel("Category")
    plt.ylabel("Activity Rate (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "activity_rate_by_category.png"
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def _plot_top_keywords(df: pd.DataFrame, top_n: int = 10) -> Path | None:
    if "ad_keywords" not in df.columns:
        return None
    counts = df["ad_keywords"].value_counts().head(top_n)
    if counts.empty:
        return None
    plt.figure(figsize=(8, 4))
    counts.plot(kind="bar", color="#48BB78")
    plt.title(f"Top {top_n} Ad Keywords")
    plt.xlabel("Keyword")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "top_ad_keywords.png"
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def _plot_numeric_over_index(df: pd.DataFrame) -> Path | None:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return None
    col = numeric_cols[0]
    plt.figure(figsize=(8, 4))
    df[col].plot(kind="line", color="#9F7AEA")
    plt.title(f"{col} over index")
    plt.xlabel("Index")
    plt.ylabel(col)
    plt.tight_layout()
    path = OUTPUT_DIR / f"{col}_over_index.png"
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def generate_charts(df: pd.DataFrame) -> List[Path]:
    paths: List[Path] = []
    for fn in (_plot_category_counts, _plot_category_conversion, _plot_top_keywords, _plot_numeric_over_index):
        p = fn(df)
        if p is not None:
            paths.append(p)
    return paths

