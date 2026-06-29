import argparse
import sys
from datetime import date
from typing import Optional

from config import (
    KEYWORDS,
    OUTPUT_DIR,
    SAVE_MAX_RESULTS_PER_KEYWORD,
    SEARCH_MAX_RESULTS_PER_KEYWORD,
)
from src.arxiv_client import ArxivClient
from src.logger import configure_logging, get_logger
from src.translator import DeepSeekTranslator
from src.utils import format_date_for_filename, parse_cli_date
from src.writer import write_markdown_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch arXiv papers by keyword and translate abstracts with DeepSeek."
    )
    parser.add_argument(
        "--date",
        dest="target_date",
        help="Target date in YYMMDD format, for example 260625.",
    )
    return parser.parse_args()


def resolve_target_date(raw_value: Optional[str]) -> date:
    if not raw_value:
        return date.today()
    return parse_cli_date(raw_value)


def main() -> int:
    configure_logging()
    logger = get_logger(__name__)
    args = parse_args()

    try:
        target_date = resolve_target_date(args.target_date) if args.target_date else None
        client = ArxivClient()
        translator = DeepSeekTranslator()

        if target_date is None:
            logger.info("Target date: latest available papers")
        else:
            logger.info("Target date: %s", target_date.isoformat())
        results = {}
        total_papers = 0

        for keyword in KEYWORDS:
            logger.info("Fetching papers for keyword: %s", keyword)
            papers = client.fetch_papers(
                keyword=keyword,
                target_date=target_date,
                max_results=SEARCH_MAX_RESULTS_PER_KEYWORD,
            )
            papers = papers[:SAVE_MAX_RESULTS_PER_KEYWORD]
            logger.info("Matched %s papers for keyword: %s", len(papers), keyword)

            for paper in papers:
                paper.abstract_zh = translator.translate_abstract(paper.abstract_en)

            results[keyword] = papers
            total_papers += len(papers)

        output_path = write_markdown_report(
            output_dir=OUTPUT_DIR,
            filename=format_date_for_filename(resolve_target_date(args.target_date)),
            target_date=target_date,
            keyword_results=results,
            total_papers=total_papers,
        )
        logger.info("Report written to %s", output_path)
        return 0
    except Exception as exc:
        logger.exception("Run failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
