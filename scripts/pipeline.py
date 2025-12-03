from pathlib import Path
from typing import Iterable, List

import pandas as pd

from create_charts import generate_charts
from generate_pdf import build_pdf
from generate_slides import build_presentation
from utils import clean_data, load_csv

INPUT_DIR = Path("data") / "input"
OUTPUT_DIR = Path("data") / "output"
CLEAN_DATASET_PATH = OUTPUT_DIR / "cleaned_dataset.csv"


def _ensure_directories() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def derive_basic_insights(df: pd.DataFrame) -> List[str]:
    insights: List[str] = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        return ["Dataset loaded successfully, but no numeric metrics were detected."]

    for column in numeric_cols[:3]: 
        trend = df[column].pct_change().mean()
        trend_pct = trend * 100 if pd.notna(trend) else 0
        insights.append(
            f"{column}: avg {df[column].mean():.2f}, "
            f"change ~{trend_pct:.1f}% over the observed period."
        )

    max_col = max(numeric_cols, key=lambda col: df[col].mean())
    insights.append(f"{max_col} is the strongest performer based on average value.")
    return insights


def save_clean_dataset(df: pd.DataFrame) -> Path:
    CLEAN_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DATASET_PATH, index=False)
    return CLEAN_DATASET_PATH


def run_pipeline(folder: str | Path = INPUT_DIR) -> None:

    _ensure_directories()
    folder_path = str(folder)

    print(f"[INGEST] Scanning {folder_path} for CSV files")
    raw_df = load_csv(folder_path)

    print("[CLEAN] Applying standard cleaning operations")
    cleaned_df = clean_data(raw_df)
    save_clean_dataset(cleaned_df)

    print("[INSIGHT] Generating quick-win insights")
    insights = derive_basic_insights(cleaned_df)

    print("[VISUALS] Rendering charts")
    chart_paths = generate_charts(cleaned_df)

    print("[REPORT] Building presentation")
    presentation_path = build_presentation(insights, chart_paths)

    print("[REPORT] Building PDF")
    pdf_path = build_pdf(insights, chart_paths)

    print("Pipeline completed successfully.")
    print(f"Clean dataset: {CLEAN_DATASET_PATH}")
    print(f"Charts: {[str(path) for path in chart_paths]}")
    print(f"Presentation: {presentation_path}")
    print(f"PDF report: {pdf_path}")

if __name__ == "__main__":
    run_pipeline()

