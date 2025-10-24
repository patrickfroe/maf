"""Minimal agent application wiring storage and skills together."""

from __future__ import annotations

from typing import Dict

from .skills.base import BaseSkill
from .storage.base import BaseStorage
from .storage.in_memory import InMemoryStorage


class AgentApp:
    """Simple agent application managing skills and shared storage."""

    def __init__(self, storage: BaseStorage | None = None) -> None:
        self.storage: BaseStorage = storage or InMemoryStorage()
        self._skills: Dict[str, BaseSkill] = {}

    def register_skill(self, skill: BaseSkill) -> None:
        self._skills[skill.metadata.name] = skill

    def get_skill(self, name: str) -> BaseSkill:
        try:
            return self._skills[name]
        except KeyError as exc:
            raise KeyError(f"Skill '{name}' is not registered") from exc

    def invoke(self, name: str, message: str) -> str:
        skill = self.get_skill(name)
        return skill.handle(message=message, storage=self.storage)


__all__ = ["AgentApp"]
