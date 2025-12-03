## H-001 InsightForge | The Automated Insight Engine

Track: Data Engineering & Analytics

## 1. Context & Problem

AdTech businesses produce massive amounts of data every day—campaign logs, clickstreams, footfall metrics, and even weather signals.
But there’s a major inefficiency:
Account Managers still manually download CSV files, clean them, create charts, and assemble “Weekly Performance Reports” for clients.

This takes 4–6 hours per week per client, delays decisions, and increases the chance of errors.

InsightForge solves this.
You drop raw data into the system, and within seconds, you get a polished PDF or PPT deck with insights, charts, and AI-generated explanations.

## 2. Expected End Result

Input:
A raw CSV file (or SQL export) dropped into an input folder or uploaded via an interface.

Action:
The system detects the new file → processes the data → generates insights.

Output:
A professional PDF/PPT containing:

Clean trend charts

Growth/decline summaries

Outlier detection (unusual spikes/drops)

AI-generated narrative explaining the patterns

Optional cross-reference with external data (like weather or region-wise events)

The goal:
Eliminate manual reporting. Produce analyst-level insights automatically.

### 3. Technical Approach

InsightForge is built as a simple, reliable ETL pipeline, not just a Python script.

1. Ingestion (Automated Trigger)

A watcher script monitors the input/ directory.
When a file arrives, the pipeline starts automatically—no buttons, no UI clicks.

2. Processing Layer

Uses Polars (faster than Pandas) to load and clean data.

Performs type validation to prevent corrupted CSVs from breaking the pipeline.

Computes metrics like CTR, conversion rates, regional performance, etc.

3. Anomaly Detection

Isolation Forest (Scikit-Learn) identifies unusual spikes/drops.

Summaries like: “Engagement dropped 38% in Region B on 12 Oct.”

4. Insight Generation (AI Layer)

AI models like GPT-4o or Gemini generate:

Natural language summaries

Explanations for patterns

Plain-English insights clients can understand

A “strict context” prompt prevents hallucinations by forcing the AI to use only the provided dataset summary.

5. Report Creation

HTML/CSS template rendered to PDF (WeasyPrint)
OR

Auto-generated PowerPoint deck (python-pptx)

Includes charts, tables, and analyst-style text.

4. Tech Stack
Component	Tool
Language	Python 3.11
Data Processing	Polars / Pandas
ML	Scikit-Learn (Isolation Forest)
AI	GPT-4o or Gemini
Visualization	Plotly / Matplotlib
Reporting	WeasyPrint (PDF), python-pptx (PPTX)
Automation	Watchdog
Optional	Docker for full pipeline isolation
5. Challenges & Learnings
1. Handling Messy Real-World Data

Different CSV formats caused schema mismatches.
Solution: added strict validation + automatic type casting.

2. AI Hallucinations

Early tests showed AI inventing reasons for trends.
Fixed using a strict JSON input + “use only provided data” guardrail.

3. File-Based Triggering

Ensuring the watcher didn’t reprocess the same file twice required ID-based caching.
