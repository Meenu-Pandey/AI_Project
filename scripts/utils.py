from pathlib import Path
from typing import List, Union
import sqlite3

import pandas as pd


def load_csv(folder_path: Union[str, Path]) -> pd.DataFrame:
    folder = Path(folder_path)
    df_list: List[pd.DataFrame] = []

    for file in sorted(folder.glob("*.csv")):
        try:
            df_list.append(pd.read_csv(file))
        except Exception as e:
            print(f"[WARN] Failed to read CSV {file.name}: {e}")

    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def load_excel(folder_path: Union[str, Path]) -> pd.DataFrame:
    folder = Path(folder_path)
    df_list: List[pd.DataFrame] = []

    for file in sorted(folder.glob("*.xlsx")):
        try:
            df_list.append(pd.read_excel(file))
        except Exception as e:
            print(f"[WARN] Failed to read Excel {file.name}: {e}")

    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def load_json(folder_path: Union[str, Path]) -> pd.DataFrame:
    folder = Path(folder_path)
    df_list: List[pd.DataFrame] = []

    for file in sorted(folder.glob("*.json")):
        try:
            df_list.append(pd.read_json(file))
        except Exception as e:
            print(f"[WARN] Failed to read JSON {file.name}: {e}")

    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def load_sqlite(db_path: Union[str, Path], table_name: str) -> pd.DataFrame:
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"[WARN] Failed to load table {table_name} from {db_path}: {e}")
        return pd.DataFrame()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for col in cleaned.columns:
        series = cleaned[col]

        if pd.api.types.is_numeric_dtype(series):
            cleaned[col] = series.fillna(0)
        elif pd.api.types.is_datetime64_any_dtype(series) or "date" in col.lower():
            try:
                cleaned[col] = pd.to_datetime(series, errors="coerce")
            except Exception:
                pass
        else:
            cleaned[col] = series.fillna("N/A")

    return cleaned
