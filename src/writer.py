from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.models import Paper
from src.utils import format_date_for_display


def write_markdown_report(
    output_dir: Path,
    filename: str,
    target_date: Optional[date],
    keyword_results: Dict[str, List[Paper]],
    total_papers: int,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text(
        build_markdown_report(
            target_date=target_date,
            keyword_results=keyword_results,
            total_papers=total_papers,
        ),
        encoding="utf-8",
    )
    return output_path


def build_markdown_report(
    target_date: Optional[date],
    keyword_results: Dict[str, List[Paper]],
    total_papers: int,
) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# arXiv Daily Paper",
        "",
        f"- Generated at: {generated_at}",
        f"- Target date: {format_date_for_display(target_date) if target_date else 'latest available'}",
        f"- Keywords: {len(keyword_results)}",
        f"- Total papers: {total_papers}",
        "",
    ]

    for keyword, papers in keyword_results.items():
        lines.append(f"## {keyword}")
        lines.append("")

        if not papers:
            lines.append("No matching papers.")
            lines.append("")
            continue

        for index, paper in enumerate(papers, start=1):
            lines.extend(
                [
                    f"### {index}. [{paper.title}]({paper.link})",
                    "",
                    f"- Updated: {paper.updated_date.isoformat()}",
                    "",
                    "**Abstract (EN)**",
                    "",
                    paper.abstract_en,
                    "",
                    "**Abstract (ZH)**",
                    "",
                    paper.abstract_zh or "Translation failed.",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"
