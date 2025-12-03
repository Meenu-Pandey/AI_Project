from pathlib import Path
from typing import Iterable

from fpdf import FPDF

OUTPUT_PATH = Path("data") / "output" / "InsightForge_Report.pdf"


class InsightPDF(FPDF):
    def header(self) -> None:
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "InsightForge Auto Report", ln=True, align="C")
        self.ln(5)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def build_pdf(insights: Iterable[str], chart_paths: Iterable[Path]) -> Path:
    pdf = InsightPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Key Insights", ln=True)
    pdf.set_font("Helvetica", size=12)

    entries = list(insights) or ["No insights available."]
    for insight in entries:
        safe_text = (f"- {insight}").replace("–", "-")
        pdf.multi_cell(0, 8, safe_text)
    pdf.ln(5)

    for chart in chart_paths:
        pdf.add_page()
        title = chart.stem.replace("_", " ").title()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.image(str(chart), x=15, y=28, w=180)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PATH))
    return OUTPUT_PATH