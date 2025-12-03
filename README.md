# InsightForge | The Automated Insight Engine

**Track:** Data Engineering & Analytics

**Tagline:** Transform raw AdTech data into analyst-ready insights in seconds.

---

## 1. Context & Problem

AdTech businesses generate massive volumes of data daily—campaign logs, clickstreams, footfall metrics, and even weather signals.

Yet, Account Managers spend **4–6 hours per client each week** manually downloading CSVs, cleaning data, creating charts, and assembling “Weekly Performance Reports.”

This manual workflow delays decisions and introduces errors.

**InsightForge** automates this process: drop raw data into the system and receive a polished PDF or PPT deck with insights, charts, and AI-generated explanations **within seconds**.

---

## 2. Expected End Result

**Input:**

* Raw CSV file or SQL export via input folder or upload interface

**Action:**

* Automatic detection → data processing → insight generation

**Output:**

* Professional PDF or PPT including:

  * Clean trend charts
  * Growth/decline summaries
  * Outlier detection (unusual spikes/drops)
  * AI-generated narrative explaining patterns
  * Optional external cross-references (e.g., weather, events)

**Goal:**
Eliminate manual reporting and produce analyst-level insights automatically.

---

## 3. Technical Approach

### 1. Ingestion (Automated Trigger)

* Watcher script monitors `input/` folder
* Pipeline starts automatically when a new file arrives

### 2. Processing Layer

* **Polars** (faster than Pandas) loads and cleans data
* Type validation prevents corrupted CSVs from breaking the pipeline
* Computes metrics: CTR, conversion rates, regional performance, etc.

### 3. Anomaly Detection

* **Isolation Forest (Scikit-Learn)** identifies unusual spikes/drops
* Example: `“Engagement dropped 38% in Region B on 12 Oct.”`

### 4. Insight Generation (AI Layer)

* **GPT-4o / Gemini** generates:

  * Natural language summaries
  * Explanations for trends
  * Plain-English insights for clients
* **Strict context prompts** prevent hallucinations

### 5. Report Creation

* PDF: HTML/CSS → WeasyPrint
* PPTX: python-pptx
* Includes charts, tables, and analyst-style text

---

## 4. Tech Stack

| Component       | Tool                                 |
| --------------- | ------------------------------------ |
| Language        | Python 3.11                          |
| Data Processing | Polars / Pandas                      |
| ML              | Scikit-Learn (Isolation Forest)      |
| AI              | GPT-4o / Gemini                      |
| Visualization   | Plotly / Matplotlib                  |
| Reporting       | WeasyPrint (PDF), python-pptx (PPTX) |
| Automation      | Watchdog                             |
| Optional        | Docker for full pipeline isolation   |

---

## 5. Challenges & Learnings

1. **Messy Real-World Data**

   * Schema mismatches across CSVs → implemented strict validation and type casting

2. **AI Hallucinations**

   * Initial AI explanations invented trends → solved using JSON input + strict “use only provided data” guardrails

3. **File-Based Triggering**

   * Preventing double-processing → implemented ID-based caching

---

## 6. Visual Proof (Optional Screenshots)

Include screenshots for:

* Terminal logs detecting anomalies
* Sample extracted insights
* Final report output
* Auto-generated charts

---

## 7. How to Run

### Clone Repository

```bash
git clone https://github.com/username/insightforge.git
cd insightforge
```

### Add API Key

```bash
export AI_API_KEY="your_key_here"
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Pipeline

```bash
python watch.py
```

### Test the System

```bash
# Move a sample file to trigger the pipeline
mv sample.csv input/
```

### Using Docker

```bash
docker-compose up --build
```

---

**License:** MIT (or your choice)
**Author:** Meenu Pandey
**Contact:** [pandeymeenu057@gmail.com](mailto:pandeymeenu057@gmail.com)
