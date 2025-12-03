
from datetime import datetime
from pathlib import Path
from typing import Union

import pandas as pd

from charts import generate_charts
from generate_pdf import build_pdf
from generate_slides import build_presentation
from insights import generate_llm_insights
from utils import clean_data, load_csv, load_excel, load_json

INPUT_DIR = Path("data") / "input"
OUTPUT_DIR = Path("data") / "output"


def run_pipeline(folder: Union[str, Path] = INPUT_DIR) -> None:
    folder = Path(folder)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INGEST] Scanning {folder} for CSV/Excel/JSON files")

    df_csv = load_csv(folder)
    df_xlsx = load_excel(folder)
    df_json = load_json(folder)

    if any(not df.empty for df in (df_csv, df_xlsx, df_json)):
        frames = [df for df in (df_csv, df_xlsx, df_json) if not df.empty]
        raw_df = pd.concat(frames, ignore_index=True)
    else:
        raw_df = pd.DataFrame()

    if raw_df.empty:
        print("[ERROR] No data files found or loaded.")
        return

    print("[CLEAN] Cleaning dataset")
    cleaned_df = clean_data(raw_df)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"[META] Processing timestamp: {timestamp}")

    print("[INSIGHT] Generating insights")
    insights = generate_llm_insights(cleaned_df)

    print("[VISUALS] Generating charts")
    chart_paths = generate_charts(cleaned_df)

    print("[REPORT] Building presentation")
    ppt_path = build_presentation(insights, chart_paths)

    print("[REPORT] Building PDF")
    pdf_path = build_pdf(insights, chart_paths)

    print("Pipeline completed successfully.")
    print(f"Presentation: {ppt_path}")
    print(f"PDF: {pdf_path}")


if __name__ == "__main__":
    run_pipeline()
