"""Skill triggering a web search and persisting the gathered results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .base import BaseSkill, SkillMetadata
from ..services.search import SearchClient, SearchResult
from ..storage.base import BaseStorage


def _default_metadata() -> SkillMetadata:
    return SkillMetadata(
        name="WebSearchSkill",
        description="Führt eine Websuche durch und speichert die Ergebnisse für weitere Verarbeitung.",
    )


@dataclass
class _StoredResult:
    title: str
    url: str
    snippet: str

    @classmethod
    def from_search_result(cls, result: SearchResult) -> "_StoredResult":
        return cls(title=result.title, url=result.url, snippet=result.snippet)

    def to_dict(self) -> dict[str, str]:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


class WebSearchSkill(BaseSkill):
    """Skill that performs a web search using a configurable search client."""

    STORAGE_NAMESPACE = "web_search"
    LAST_QUERY_KEY = "__last_query__"

    def __init__(
        self,
        search_client: SearchClient | None = None,
        *,
        max_results: int = 5,
        metadata: SkillMetadata | None = None,
    ) -> None:
        super().__init__(metadata or _default_metadata())
        self._search_client = search_client
        self._max_results = max(1, max_results)

    def _resolve_client(self) -> SearchClient:
        if self._search_client is not None:
            return self._search_client

        try:
            from duckduckgo_search import DDGS  # type: ignore
        except ImportError as exc:  # pragma: no cover - exercised in integration usage only
            raise RuntimeError(
                "Die Standard-Websuche benötigt das Paket 'duckduckgo_search'. "
                "Bitte installiere es oder übergib einen eigenen SearchClient."
            ) from exc

        class _DuckDuckGoClient:
            def search(self, query: str, *, max_results: int = 5) -> Iterable[SearchResult]:
                with DDGS() as search:
                    results = search.text(query, max_results=max_results)
                for entry in results:
                    yield SearchResult(
                        title=entry.get("title", ""),
                        url=entry.get("href", ""),
                        snippet=entry.get("body", ""),
                    )

        self._search_client = _DuckDuckGoClient()
        return self._search_client

    def handle(self, message: str, storage: BaseStorage, **_: object) -> str:
        query = message.strip()
        if not query:
            return "Bitte gib ein Suchthema an, um eine Websuche zu starten."

        try:
            client = self._resolve_client()
        except RuntimeError as exc:
            return str(exc)
        results = list(client.search(query, max_results=self._max_results))
        stored_results = [
            _StoredResult.from_search_result(result).to_dict() for result in results if result.title or result.url
        ]

        storage.set(self.STORAGE_NAMESPACE, query, stored_results)
        storage.set(self.STORAGE_NAMESPACE, self.LAST_QUERY_KEY, query)

        if not stored_results:
            return f"Keine Treffer für '{query}' gefunden."

        return self._format_response(query, stored_results)

    def _format_response(self, query: str, results: list[dict[str, str]]) -> str:
        lines = [f"Suchergebnisse für '{query}':"]
        for entry in results:
            title = entry.get("title", "Unbenannter Treffer")
            url = entry.get("url", "")
            snippet = entry.get("snippet", "").strip()
            if len(snippet) > 180:
                snippet = f"{snippet[:177]}..."
            link_segment = f" ({url})" if url else ""
            lines.append(f"- {title}{link_segment}: {snippet}")
        return "\n".join(lines)


__all__ = ["WebSearchSkill"]

