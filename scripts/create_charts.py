from pathlib import Path
from typing import Iterable, List

import matplotlib.pyplot as plt
import pandas as pd

CHART_DIR = Path("data") / "output" / "charts"


def _ensure_dir(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _is_datetime_series(series: pd.Series) -> bool:
    return pd.api.types.is_datetime64_any_dtype(series)


def _first_datetime_column(df: pd.DataFrame) -> str | None:
    for column in df.columns:
        if _is_datetime_series(df[column]):
            return column
    return None


def _numeric_columns(df: pd.DataFrame) -> List[str]:
    return df.select_dtypes(include="number").columns.tolist()


def _save_plot(name: str) -> Path:
    return _ensure_dir(CHART_DIR) / f"{name}.png"


def _plot_numeric_summary(df: pd.DataFrame) -> Path | None:
    numeric_cols = _numeric_columns(df)
    if not numeric_cols:
        return None

    means = df[numeric_cols].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 4))
    means.plot(kind="bar", color="#4FED84")
    plt.title("Average Metrics by Column")
    plt.tight_layout()

    output_path = _save_plot("numeric_summary")
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def _plot_time_series(df: pd.DataFrame) -> Path | None:
    column = _first_datetime_column(df)
    numeric_cols = _numeric_columns(df)
    if column is None or not numeric_cols:
        return None

    metric = numeric_cols[0]
    time_df = df[[column, metric]].sort_values(column)

    plt.figure(figsize=(8, 4))
    plt.plot(time_df[column], time_df[metric], marker="o", color="#F6AD55")
    plt.title(f"{metric} over Time")
    plt.xlabel(column.title())
    plt.ylabel(metric.title())
    plt.xticks(rotation=30)
    plt.tight_layout()

    output_path = _save_plot("time_series")
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def generate_charts(df: pd.DataFrame) -> List[Path]:
    paths: Iterable[Path | None] = [_plot_numeric_summary(df), _plot_time_series(df)]
    return [path for path in paths if path is not None]