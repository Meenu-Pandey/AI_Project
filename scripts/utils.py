import os
import pandas as pd

def load_csv(folder_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    df_list = []

    for file in all_files:
        try:
            df = pd.read_csv(os.path.join(folder_path, file))
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    combined_df = pd.concat(df_list, ignore_index=True)
    print(combined_df.head())
    return combined_df


def clean_data(df):
    cleaned_df = df.copy().fillna(0)

    for column in cleaned_df.columns:
        if "date" in column.lower():
            try:
                cleaned_df[column] = pd.to_datetime(cleaned_df[column], errors="coerce")
            except Exception as e:
                print(f"Error converting {column} to datetime: {e}")

    return cleaned_df

