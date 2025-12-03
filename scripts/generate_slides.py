from pathlib import Path
from typing import Iterable

from pptx import Presentation
from pptx.util import Inches

OUTPUT_PATH = Path("data") / "output" / "InsightForge_Report.pptx"


def build_presentation(insights: Iterable[str], chart_paths: Iterable[Path]) -> Path:
    prs = Presentation()

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "InsightForge Auto Report"
    slide.placeholders[1].text = "Generated via Insight Engine"

    # Insights slide
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Insights"
    body = slide.shapes.placeholders[1].text_frame
    body.clear()

    entries = list(insights) or ["No insights available."]
    for i, insight in enumerate(entries):
        if i == 0:
            body.text = insight
        else:
            body.add_paragraph().text = insight

    # Chart slides with titles based on chart filenames
    for chart in chart_paths:
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = chart.stem.replace("_", " ").title()
        left = Inches(1)
        top = Inches(1.0)
        slide.shapes.add_picture(str(chart), left, top, width=Inches(8))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PATH)
    return OUTPUT_PATH