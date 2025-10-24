"""Base definitions for agent skills."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..storage.base import BaseStorage


@dataclass
class SkillMetadata:
    """Metadata describing a skill.

    Attributes:
        name: Human readable name of the skill.
        description: Short explanation of what the skill does.
    """

    name: str
    description: str


class BaseSkill(ABC):
    """Base class for skills used by the demo agent app."""

    def __init__(self, metadata: SkillMetadata) -> None:
        self._metadata = metadata

    @property
    def metadata(self) -> SkillMetadata:
        """Return the metadata for the skill."""

        return self._metadata

    @abstractmethod
    def handle(self, message: str, storage: BaseStorage, **kwargs: Any) -> str:
        """Process an incoming message and return a response."""


__all__ = ["SkillMetadata", "BaseSkill"]
