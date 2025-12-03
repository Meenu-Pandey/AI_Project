from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import json

import pandas as pd

try:
    import openai  # type: ignore
except ImportError:  # pragma: no cover
    openai = None


@dataclass
class InsightSections:
    overview: List[str]
    key_metrics: List[str]
    trends: List[str]
    anomalies: List[str]
    recommendations: List[str]
    summary: List[str]

    def as_bullets(self) -> List[str]:
        bullets: List[str] = []
        for section in (
            self.overview,
            self.key_metrics,
            self.trends,
            self.anomalies,
            self.recommendations,
            self.summary,
        ):
            bullets.extend(section)
        return bullets


def _fallback_insights(df: pd.DataFrame) -> InsightSections:
    overview: List[str] = []
    key_metrics: List[str] = []
    trends: List[str] = []
    anomalies: List[str] = []
    recommendations: List[str] = []
    summary: List[str] = []

    total_rows = len(df)
    if "category" in df.columns:
        category_note = f"{df['category'].nunique()} categories"
    else:
        category_note = "mixed feature set"
    overview.append(f"Ingested {total_rows:,} rows covering {category_note}.")

    if "activity" in df.columns:
        activity_rate = df["activity"].mean() * 100
        key_metrics.append(f"Portfolio-wide activity rate sits at {activity_rate:.1f}%.")
        if "category" in df.columns:
            cat_perf = (
                df.groupby("category")["activity"].mean().sort_values(ascending=False) * 100
            )
            best_cat = cat_perf.index[0]
            worst_cat = cat_perf.index[-1]
            trends.append(
                f"{best_cat} leads with {cat_perf.iloc[0]:.1f}% activation vs. "
                f"{worst_cat} at {cat_perf.iloc[-1]:.1f}%."
            )
            std = cat_perf.std()
            threshold_high = cat_perf.mean() + std
            threshold_low = cat_perf.mean() - std
            high_outliers = cat_perf[cat_perf >= threshold_high]
            low_outliers = cat_perf[cat_perf <= threshold_low]
            for cat, rate in high_outliers.items():
                anomalies.append(f"{cat} outperforms materially at {rate:.1f}% activation.")
            for cat, rate in low_outliers.items():
                anomalies.append(f"{cat} under-indexes at {rate:.1f}% activation.")
        if "ad_keywords" in df.columns:
            kw_perf = (
                df.groupby("ad_keywords")["activity"]
                .agg(["mean", "count"])
                .query("count >= 5")
                .sort_values("mean", ascending=False)
            )
            if not kw_perf.empty:
                top_kw = kw_perf.index[0]
                key_metrics.append(
                    f"Keyword '{top_kw}' tops conversion at {kw_perf.iloc[0]['mean']*100:.1f}%."
                )
                rec_low = kw_perf.tail(1).index[0]
                recommendations.append(
                    f"Reallocate spend from '{rec_low}' into '{top_kw}' to lift ROI."
                )
    else:
        overview.append("Activity column missing; showing structural metrics only.")

    summary.append("Dataset processed successfully; see recommendations for next best actions.")
    if not recommendations:
        recommendations.append("Prioritize best-performing categories while shoring up laggards.")

    return InsightSections(
        overview=overview,
        key_metrics=key_metrics,
        trends=trends,
        anomalies=anomalies,
        recommendations=recommendations,
        summary=summary,
    )


def _build_prompt(metrics: Dict[str, str]) -> str:
    return f"""
You are an executive insights partner at a top-tier consulting firm.
Craft concise narrative bullets for a C-level weekly business review.
Use the following structured data summary and respond in JSON with keys:
overview, key_metrics, trends, anomalies, recommendations, summary.
Each key should contain an array of 2-4 punchy bullet strings (max 160 chars each).
Prioritise comparisons, cause/effect, and actionable recommendations.
Avoid generic statements. Sound confident and data-backed.

DATA SUMMARY:
{metrics}
"""


def _collect_metrics(df: pd.DataFrame) -> Dict[str, str]:
    metrics: Dict[str, str] = {}
    metrics["row_count"] = str(len(df))
    for col in ("category", "ad_keywords"):
        if col in df.columns:
            metrics[f"{col}_unique"] = str(df[col].nunique())
    if "activity" in df.columns:
        metrics["activity_rate"] = f"{df['activity'].mean() * 100:.2f}"
        metrics["active_volume"] = str(int(df["activity"].sum()))
        metrics["inactive_volume"] = str(int((1 - df["activity"]) .sum()))
    if {"activity", "category"}.issubset(df.columns):
        top_cat = (
            df.groupby("category")["activity"].mean().sort_values(ascending=False).head(3)
        )
        metrics["top_categories"] = ", ".join(
            f"{idx}:{val*100:.1f}%" for idx, val in top_cat.items()
        )
    if {"activity", "ad_keywords"}.issubset(df.columns):
        top_kw = (
            df.groupby("ad_keywords")["activity"]
            .mean()
            .sort_values(ascending=False)
            .head(5)
        )
        metrics["top_keywords"] = ", ".join(
            f"{idx}:{val*100:.1f}%" for idx, val in top_kw.items()
        )
    return metrics


def _invoke_llm(prompt: str) -> Optional[InsightSections]:
    if openai is None:
        return None
    try:
        completion = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an executive insights generator."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=600,
        )
        content = completion.choices[0].message["content"]  # type: ignore[index]
        data = json.loads(content)
        return InsightSections(
            overview=list(data.get("overview", [])),
            key_metrics=list(data.get("key_metrics", [])),
            trends=list(data.get("trends", [])),
            anomalies=list(data.get("anomalies", [])),
            recommendations=list(data.get("recommendations", [])),
            summary=list(data.get("summary", [])),
        )
    except Exception:
        return None


def generate_llm_insights(df: pd.DataFrame) -> InsightSections:
    metrics = _collect_metrics(df)
    prompt = _build_prompt(metrics)
    llm_result = _invoke_llm(prompt)
    if llm_result:
        return llm_result
    return _fallback_insights(df)