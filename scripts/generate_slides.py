from pathlib import Path
from typing import Iterable, List

from pptx import Presentation
from pptx.util import Inches, Pt

OUTPUT_PATH = Path("data") / "output" / "InsightForge_Report.pptx"

def _ensure_output_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _add_title_slide(prs: Presentation, title: str, subtitle: str) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle


def _add_insights_slide(prs: Presentation, insights: Iterable[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Insights"
    body = slide.shapes.placeholders[1].text_frame
    body.clear()

    for index, insight in enumerate(insights):
        if index == 0:
            body.text = insight
        else:
            body.add_paragraph().text = insight


def _add_chart_slide(prs: Presentation, chart_path: Path) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = chart_path.stem.replace("_", " ").title()
    left = Inches(1)
    top = Inches(1.5)
    slide.shapes.add_picture(str(chart_path), left, top, width=Inches(8))


def build_presentation(insights: Iterable[str], chart_paths: Iterable[Path]) -> Path:
    prs = Presentation()
    _add_title_slide(prs, "InsightForge Auto Report", "Generated via Insight Engine")
    _add_insights_slide(prs, list(insights) or ["No insights available."])

    for chart in chart_paths:
        _add_chart_slide(prs, chart)

    _ensure_output_dir(OUTPUT_PATH)
    prs.save(OUTPUT_PATH)
    return OUTPUT_PATH