"""Implementation of a simple echo skill."""

from __future__ import annotations

from typing import Any

from .base import BaseSkill, SkillMetadata
from ..storage.base import BaseStorage


def _default_metadata() -> SkillMetadata:
    return SkillMetadata(
        name="EchoSkill",
        description="Returns the exact input back to the caller and stores a history of messages.",
    )


class EchoSkill(BaseSkill):
    """Skill that echoes the input message and persists the conversation history."""

    HISTORY_NAMESPACE = "echo"
    HISTORY_KEY = "history"

    def __init__(self, metadata: SkillMetadata | None = None) -> None:
        super().__init__(metadata or _default_metadata())

    def handle(self, message: str, storage: BaseStorage, **_: Any) -> str:
        history = storage.get(self.HISTORY_NAMESPACE, self.HISTORY_KEY)
        if history is None:
            history = []
        history.append(message)
        storage.set(self.HISTORY_NAMESPACE, self.HISTORY_KEY, history)
        return message

    def conversation_history(self, storage: BaseStorage) -> list[str]:
        history = storage.get(self.HISTORY_NAMESPACE, self.HISTORY_KEY)
        return list(history or [])


__all__ = ["EchoSkill"]
