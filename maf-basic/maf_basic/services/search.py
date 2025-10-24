"""Search service abstractions used by the web search skill."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass(frozen=True)
class SearchResult:
    """Container describing a single search result entry."""

    title: str
    url: str
    snippet: str

    def as_dict(self) -> dict[str, str]:
        """Return a serialisable representation of the result."""

        return {"title": self.title, "url": self.url, "snippet": self.snippet}


class SearchClient(Protocol):
    """Protocol that needs to be implemented by search providers."""

    def search(self, query: str, *, max_results: int = 5) -> Iterable[SearchResult]:
        """Return an iterable of :class:`SearchResult` objects."""


__all__ = ["SearchResult", "SearchClient"]

