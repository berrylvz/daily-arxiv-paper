from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

import feedparser
import requests

from config import ARXIV_BASE_URL, REQUEST_TIMEOUT, RETRY_TIMES, TARGET_PRIMARY_CATEGORIES
from src.logger import get_logger
from src.models import Paper
from src.utils import clean_text


class ArxivClient:
    def __init__(self) -> None:
        self.logger = get_logger(__name__)

    def fetch_papers(
        self, keyword: str, target_date: Optional[date], max_results: int
    ) -> List[Paper]:
        params = {
            "search_query": f'all:"{keyword}"',
            "start": 0,
            "max_results": max_results,
            "sortBy": "lastUpdatedDate",
            "sortOrder": "descending",
        }

        last_error: Optional[Exception] = None
        for attempt in range(1, RETRY_TIMES + 1):
            try:
                response = requests.get(
                    ARXIV_BASE_URL,
                    params=params,
                    timeout=REQUEST_TIMEOUT,
                )
                response.raise_for_status()
                return self._parse_feed(response.text, target_date)
            except requests.RequestException as exc:
                last_error = exc
                self.logger.warning(
                    "arXiv request failed for keyword '%s' (attempt %s/%s): %s",
                    keyword,
                    attempt,
                    RETRY_TIMES,
                    exc,
                )

        raise RuntimeError(f"Failed to fetch arXiv papers for '{keyword}'.") from last_error

    def _parse_feed(self, payload: str, target_date: Optional[date]) -> List[Paper]:
        feed = feedparser.parse(payload)
        papers: List[Paper] = []

        for entry in feed.entries:
            updated_raw = getattr(entry, "updated", "")
            if not updated_raw:
                continue

            updated_date = datetime.strptime(updated_raw, "%Y-%m-%dT%H:%M:%SZ").date()
            if target_date is not None and updated_date != target_date:
                continue
            if not self._matches_target_categories(entry):
                continue

            papers.append(
                Paper(
                    title=clean_text(getattr(entry, "title", "")),
                    link=clean_text(getattr(entry, "link", "")),
                    abstract_en=clean_text(getattr(entry, "summary", "")),
                    abstract_zh="",
                    updated_date=updated_date,
                )
            )

        return papers

    def _matches_target_categories(self, entry: object) -> bool:
        tags = getattr(entry, "tags", [])
        for tag in tags:
            term = clean_text(getattr(tag, "term", ""))
            if term and term.split(".", 1)[0] in TARGET_PRIMARY_CATEGORIES:
                return True
        return False
