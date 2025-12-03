from datetime import datetime
from pathlib import Path
from typing import Iterable

from fpdf import FPDF

from charts import ChartArtifact
from insights import InsightSections

OUTPUT_PATH = Path("data") / "output" / "InsightForge_Report.pdf"

ACCENT_RGB = (31, 78, 121)


def _safe(text: str) -> str:
    return (
        text.replace("•", "-")
        .replace("–", "-")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


class InsightPDF(FPDF):
    def header(self) -> None:
        pass  # custom cover pages handle headers

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*ACCENT_RGB)
        self.cell(0, 10, _safe(f"InsightForge - Page {self.page_no()}"), align="C")


def _add_cover(pdf: InsightPDF, timestamp: str) -> None:
    pdf.add_page()
    pdf.set_fill_color(*ACCENT_RGB)
    pdf.rect(0, 0, pdf.w, 40, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.ln(12)
    pdf.cell(0, 10, _safe("InsightForge Executive Brief"), ln=True, align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, _safe(f"Generated {timestamp}"), ln=True, align="C")
    pdf.ln(40)
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(
        0,
        8,
        _safe(
            "Automated performance review spanning overview, key metrics, "
            "trend diagnostics, anomalies, and recommended next actions."
        ),
        align="C",
    )


def _add_summary_page(pdf: InsightPDF, title: str, blocks: Iterable[tuple[str, Iterable[str]]]) -> None:
    available = [(heading, [b for b in bullets if b.strip()]) for heading, bullets in blocks]
    available = [(h, items[:6]) for h, items in available if items]
    if not available:
        return

    pdf.add_page()
    pdf.set_text_color(*ACCENT_RGB)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, _safe(title), ln=True)
    pdf.ln(3)

    for heading, items in available:
        pdf.set_text_color(*ACCENT_RGB)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, _safe(heading), ln=True)
        pdf.ln(1)
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", size=12)
        for bullet in items:
            pdf.multi_cell(0, 7, _safe("- " + bullet))
        pdf.ln(2)


def _add_chart_page(pdf: InsightPDF, chart: ChartArtifact) -> None:
    pdf.add_page()
    pdf.set_text_color(*ACCENT_RGB)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _safe(chart.title), ln=True)
    pdf.ln(2)
    pdf.image(str(chart.path), x=15, y=30, w=180)
    pdf.set_y(150)
    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 8, _safe(chart.description))


def build_pdf(insights: InsightSections, charts: Iterable[ChartArtifact]) -> Path:
    pdf = InsightPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    timestamp = datetime.now().strftime("%d %b %Y %H:%M")

    _add_cover(pdf, timestamp)
    _add_summary_page(
        pdf,
        "Executive Snapshot",
        [
            ("Overview", insights.overview),
            ("Key Metrics", insights.key_metrics),
            ("Trend Diagnostics", insights.trends),
        ],
    )
    _add_summary_page(
        pdf,
        "Risks & Recommended Plays",
        [
            ("Anomalies & Watchouts", insights.anomalies),
            ("Strategic Recommendations", insights.recommendations),
            ("Closing Summary", insights.summary),
        ],
    )

    for chart in charts:
        _add_chart_page(pdf, chart)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PATH))
    return OUTPUT_PATH