from typing import List

import pandas as pd


def generate_llm_insights(df: pd.DataFrame, max_columns: int = 5) -> List[str]:
    insights: List[str] = []

    if "activity" not in df.columns:
        return ["No 'activity' column found; cannot compute engagement insights."]

    activity = df["activity"].dropna()
    if activity.empty:
        return ["Activity column is empty; no engagement insights available."]

    overall_rate = activity.mean() * 100
    insights.append(f"Overall activity rate: {overall_rate:.1f}% of events are active (1).")

    if "category" in df.columns:
        cat_stats = (
            df.groupby("category")["activity"]
            .agg(["mean", "count"])
            .sort_values("mean", ascending=False)
        )
        top_cats = cat_stats.head(3)
        for cat, row in top_cats.iterrows():
            insights.append(
                f"Category '{cat}' – activity rate {row['mean'] * 100:.1f}% "
                f"across {int(row['count'])} events."
            )
        low_cats = cat_stats.tail(3)
        for cat, row in low_cats.iterrows():
            insights.append(
                f"Category '{cat}' is weaker – activity rate {row['mean'] * 100:.1f}% "
                f"across {int(row['count'])} events."
            )

    if "ad_keywords" in df.columns:
        kw_stats = (
            df.groupby("ad_keywords")["activity"]
            .agg(["mean", "count"])
            .query("count >= 10")
            .sort_values("mean", ascending=False)
        )
        top_kw = kw_stats.head(min(max_columns, len(kw_stats)))
        for kw, row in top_kw.iterrows():
            insights.append(
                f"Keyword '{kw}' – activity rate {row['mean'] * 100:.1f}% "
                f"over {int(row['count'])} events."
            )

    if not insights:
        return ["No meaningful engagement patterns detected in the current dataset."]

    return insights

