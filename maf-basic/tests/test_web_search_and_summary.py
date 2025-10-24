"""Tests covering the interplay between the web search and summary skills."""

from __future__ import annotations

import pathlib
import sys
from typing import Iterable

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maf_basic.skills.management_summary import ManagementSummarySkill
from maf_basic.skills.web_search import WebSearchSkill
from maf_basic.services.search import SearchResult
from maf_basic.storage.in_memory import InMemoryStorage


class FakeSearchClient:
    def __init__(self, results: Iterable[SearchResult]) -> None:
        self._results = list(results)
        self.queries: list[str] = []

    def search(self, query: str, *, max_results: int = 5) -> Iterable[SearchResult]:
        self.queries.append(query)
        return self._results[:max_results]


@pytest.fixture()
def storage() -> InMemoryStorage:
    return InMemoryStorage()


def test_web_search_skill_stores_results(storage: InMemoryStorage) -> None:
    client = FakeSearchClient(
        results=[
            SearchResult(title="Result 1", url="https://example.com/1", snippet="First finding about AI."),
            SearchResult(title="Result 2", url="https://example.com/2", snippet="Second finding about AI."),
        ]
    )
    skill = WebSearchSkill(search_client=client, max_results=2)

    response = skill.handle("Aktuelle KI Trends", storage)

    assert "Suchergebnisse für 'Aktuelle KI Trends'" in response
    stored = storage.get(WebSearchSkill.STORAGE_NAMESPACE, "Aktuelle KI Trends")
    assert stored == [
        {
            "title": "Result 1",
            "url": "https://example.com/1",
            "snippet": "First finding about AI.",
        },
        {
            "title": "Result 2",
            "url": "https://example.com/2",
            "snippet": "Second finding about AI.",
        },
    ]


def test_summary_skill_builds_management_summary(storage: InMemoryStorage) -> None:
    results = [
        {
            "title": "Result 1",
            "url": "https://example.com/1",
            "snippet": "First finding about AI.",
        },
        {
            "title": "Result 2",
            "url": "https://example.com/2",
            "snippet": "Second finding about AI.",
        },
    ]
    storage.set(WebSearchSkill.STORAGE_NAMESPACE, "Aktuelle KI Trends", results)
    storage.set(WebSearchSkill.STORAGE_NAMESPACE, WebSearchSkill.LAST_QUERY_KEY, "Aktuelle KI Trends")

    summary_skill = ManagementSummarySkill(max_items=2)
    summary = summary_skill.handle("Aktuelle KI Trends", storage)

    assert "Management Summary zu 'Aktuelle KI Trends'" in summary
    assert "- Result 1: First finding about AI." in summary
    assert "- Result 2: Second finding about AI." in summary


def test_summary_without_explicit_topic_uses_last_query(storage: InMemoryStorage) -> None:
    storage.set(WebSearchSkill.STORAGE_NAMESPACE, WebSearchSkill.LAST_QUERY_KEY, "Aktuelle KI Trends")
    storage.set(
        WebSearchSkill.STORAGE_NAMESPACE,
        "Aktuelle KI Trends",
        [{"title": "Result 1", "url": "", "snippet": "First finding about AI."}],
    )

    summary_skill = ManagementSummarySkill(max_items=1)
    summary = summary_skill.handle("", storage)

    assert "Management Summary zu 'Aktuelle KI Trends'" in summary
    assert "First finding about AI." in summary


def test_summary_handles_missing_results(storage: InMemoryStorage) -> None:
    summary_skill = ManagementSummarySkill()
    response = summary_skill.handle("Unbekanntes Thema", storage)

    assert "Keine gespeicherten Suchergebnisse" in response
