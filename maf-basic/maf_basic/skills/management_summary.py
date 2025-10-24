"""Skill that produces a management level summary from stored search results."""

from __future__ import annotations

from collections.abc import Sequence

from .base import BaseSkill, SkillMetadata
from .web_search import WebSearchSkill
from ..storage.base import BaseStorage


def _default_metadata() -> SkillMetadata:
    return SkillMetadata(
        name="ManagementSummarySkill",
        description="Fasst gespeicherte Suchergebnisse zu einer kurzen Management Summary zusammen.",
    )


class ManagementSummarySkill(BaseSkill):
    """Generate a short textual summary based on previously stored search results."""

    STORAGE_NAMESPACE = "management_summary"

    def __init__(self, metadata: SkillMetadata | None = None, *, max_items: int = 3) -> None:
        super().__init__(metadata or _default_metadata())
        self._max_items = max(1, max_items)

    def handle(self, message: str, storage: BaseStorage, **_: object) -> str:
        topic = message.strip()
        if not topic:
            topic = storage.get(WebSearchSkill.STORAGE_NAMESPACE, WebSearchSkill.LAST_QUERY_KEY) or ""

        if not topic:
            return "Keine Suchanfrage gefunden. Bitte starte zuerst eine Websuche."

        raw_results = storage.get(WebSearchSkill.STORAGE_NAMESPACE, topic)
        if not raw_results:
            return (
                f"Keine gespeicherten Suchergebnisse für '{topic}' gefunden. "
                "Führe zunächst die WebSearchSkill aus."
            )

        summary = self._build_summary(topic, raw_results[: self._max_items])
        storage.set(self.STORAGE_NAMESPACE, topic, summary)
        return "\n".join(summary)

    def _build_summary(self, topic: str, results: Sequence[dict[str, str]]) -> list[str]:
        lines = [f"Management Summary zu '{topic}':"]
        for entry in results:
            title = entry.get("title", "Eintrag ohne Titel")
            snippet = entry.get("snippet", "").strip() or "Keine Beschreibung verfügbar."
            if len(snippet) > 160:
                snippet = f"{snippet[:157]}..."
            lines.append(f"- {title}: {snippet}")
        if len(results) == 0:
            lines.append("- Keine Ergebnisse zum Zusammenfassen vorhanden.")
        return lines


__all__ = ["ManagementSummarySkill"]

