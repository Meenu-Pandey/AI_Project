from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = Path("data") / "output" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "navy": "#0B2545",
    "teal": "#1D7874",
    "gold": "#F0A202",
    "violet": "#7F3CFF",
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#EFEFF2",
        "axes.labelcolor": "#0B2545",
        "axes.titleweight": "bold",
        "ytick.color": "#4A4A4A",
        "xtick.color": "#4A4A4A",
        "figure.facecolor": "#FFFFFF",
        "grid.color": "#EFEFF2",
        "grid.linestyle": "--",
        "grid.alpha": 0.6,
    }
)


@dataclass
class ChartArtifact:
    path: Path
    title: str
    description: str


def _plot_category_counts(df: pd.DataFrame) -> Optional[ChartArtifact]:
    if "category" not in df.columns:
        return None
    counts = df["category"].value_counts().sort_values(ascending=False)
    if counts.empty:
        return None
    plt.figure(figsize=(8, 4.2))
    counts.plot(kind="bar", color=PALETTE["navy"])
    plt.title("Events by Category")
    plt.xlabel("Category")
    plt.ylabel("Volume")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "events_by_category.png"
    plt.savefig(path, dpi=220)
    plt.close()
    top_cat = counts.index[0]
    description = (
        f"{top_cat} leads in engagement volume, contributing "
        f"{counts.iloc[0]:,} logged interactions across the period."
    )
    return ChartArtifact(path, "Events by Category", description)


def _plot_category_conversion(df: pd.DataFrame) -> Optional[ChartArtifact]:
    if "category" not in df.columns or "activity" not in df.columns:
        return None
    conv = df.groupby("category")["activity"].mean().sort_values(ascending=False) * 100
    if conv.empty:
        return None
    plt.figure(figsize=(8, 4.2))
    conv.plot(kind="bar", color=PALETTE["teal"])
    plt.title("Activity Rate by Category (%)")
    plt.xlabel("Category")
    plt.ylabel("Active Share (%)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "activity_rate_by_category.png"
    plt.savefig(path, dpi=220)
    plt.close()
    best_cat = conv.index[0]
    description = (
        f"{best_cat} converts {conv.iloc[0]:.1f}% of impressions into active sessions; "
        f"median segment trails at {conv.median():.1f}%."
    )
    return ChartArtifact(path, "Activity Rate by Category", description)


def _plot_top_keywords(df: pd.DataFrame, top_n: int = 10) -> Optional[ChartArtifact]:
    if "ad_keywords" not in df.columns:
        return None
    counts = df["ad_keywords"].value_counts().head(top_n)
    if counts.empty:
        return None
    plt.figure(figsize=(8, 4.2))
    counts.plot(kind="bar", color=PALETTE["gold"])
    plt.title(f"Top {top_n} Performing Keywords")
    plt.xlabel("Keyword")
    plt.ylabel("Volume")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    path = OUTPUT_DIR / "top_ad_keywords.png"
    plt.savefig(path, dpi=220)
    plt.close()
    description = (
        f"'{counts.index[0]}' is the highest-traction creative keyword with "
        f"{counts.iloc[0]:,} logged engagements."
    )
    return ChartArtifact(path, "Top Ad Keywords", description)


def _plot_numeric_over_index(df: pd.DataFrame) -> Optional[ChartArtifact]:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return None
    col = numeric_cols[0]
    series = df[col]
    plt.figure(figsize=(8, 4.2))
    series.plot(kind="line", color=PALETTE["violet"], linewidth=2)
    plt.title(f"{col.title()} Trajectory")
    plt.xlabel("Record Index")
    plt.ylabel(col.title())
    plt.grid(True, axis="y")
    plt.tight_layout()
    path = OUTPUT_DIR / f"{col}_over_index.png"
    plt.savefig(path, dpi=220)
    plt.close()
    description = (
        f"{col.title()} spans {series.min():.0f}-{series.max():.0f} with "
        f"visible inflection around record {series.idxmax()}."
    )
    return ChartArtifact(path, f"{col.title()} Trajectory", description)


ChartFunction = Callable[[pd.DataFrame], Optional[ChartArtifact]]
CHART_BUILDERS: List[ChartFunction] = [
    _plot_category_counts,
    _plot_category_conversion,
    _plot_top_keywords,
    _plot_numeric_over_index,
]


def generate_charts(df: pd.DataFrame) -> List[ChartArtifact]:
    artifacts: List[ChartArtifact] = []
    for builder in CHART_BUILDERS:
        artifact = builder(df)
        if artifact is not None:
            artifacts.append(artifact)
    return artifacts

