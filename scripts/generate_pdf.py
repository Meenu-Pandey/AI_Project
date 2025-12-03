from pathlib import Path
from typing import Iterable

from fpdf import FPDF

OUTPUT_PATH = Path("data") / "output" / "InsightForge_Report.pdf"


def _ensure_output_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class InsightPDF(FPDF):

    def header(self) -> None:
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "InsightForge Auto Report", ln=True, align="C")
        self.ln(5)


def _add_insights_section(pdf: InsightPDF, insights: Iterable[str]) -> None:
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "Key Insights", ln=True)
    pdf.set_font("Helvetica", size=11)

    entries = list(insights) or ["No insights available."]
    for insight in entries:
        pdf.multi_cell(0, 8, f"- {insight}")
    pdf.ln(5)


def _add_chart_pages(pdf: InsightPDF, chart_paths: Iterable[Path]) -> None:
    for chart in chart_paths:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, chart.stem.replace("_", " ").title(), ln=True)
        pdf.image(str(chart), x=15, y=30, w=180)


def build_pdf(insights: Iterable[str], chart_paths: Iterable[Path]) -> Path:

    pdf = InsightPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    _add_insights_section(pdf, insights)
    _add_chart_pages(pdf, chart_paths)

    _ensure_output_dir(OUTPUT_PATH)
    pdf.output(str(OUTPUT_PATH))
    return OUTPUT_PATH