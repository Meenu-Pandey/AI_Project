# InsightForge Executive Summary

**Mission**  
Accelerate AdTech reporting by transforming raw multichannel exports into boardroom-ready insights within minutes. The automated engine ingests CSV/Excel/JSON drops, cleans & validates data, surfaces narrative intelligence (overview → metrics → anomalies → recommendations), and delivers premium PDF / PPT artifacts mirroring consulting deliverables.

**Pipeline Highlights**
1. **Smart Ingestion** – Unified loaders handle CSV, Excel, JSON (extensible to SQLite). Schema-aware cleaning standardizes numeric/date/text fields and mints a consolidated dataset for downstream analysis.
2. **Executive Insights** – An upgraded prompt strategy (with deterministic fallback) shapes C-level storytelling: overview context, portfolio metrics, comparative trend signals, anomaly detection, and action-oriented recommendations.
3. **Visual Intelligence** – Matplotlib-based chart factory outputs McKinsey-style visuals (navy/teal palette, tightened grids, copy-ready captions) tailored to the AdTech schema: category volume, conversion leaders, keyword lift, numeric trajectories.
4. **Premium Reporting** – Redesigned PPTX & PDF generators follow a structured storyline: cover → executive snapshot → metrics/trends → risks/actions → charts with narrative captions. Slides/text blocks auto-collapse when data is sparse, preventing empty whitespace.

**Narrative Enhancements**
- Cause-effect framing and cross-category comparisons drive decision clarity.
- Recommendations link outliers to capital allocation plays (e.g., reinvest in high-performing creatives, triage under-indexing segments).
- Fallback copy ensures resilience when LLM access is limited.

**Deliverables**
- `data/output/InsightForge_Report.pdf` – compact, multi-section brief with cover page, executive summary blocks, risk/action view, and annotated charts.
- `data/output/InsightForge_Report.pptx` – meeting-ready deck with harmonized typography, accent colors, and captioned visuals.
- `scripts/` modules encapsulate ingestion, insight generation, charting, and reporting logic for easy extension (watcher triggers, anomaly ML, etc.).

**Next Steps for Judges**
1. Drop sample CSVs into `data/input/`.
2. Run `python scripts/pipeline.py`.
3. Review generated PDF/PPT alongside `executive_summary.md` to assess InsightForge’s readiness for enterprise deployment.***

