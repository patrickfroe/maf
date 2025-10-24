"""Storage abstractions for the demo agent app."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseStorage(ABC):
    """Abstract storage used to persist skill state."""

    @abstractmethod
    def get(self, namespace: str, key: str) -> Optional[Any]:
        """Return a value stored under the namespace and key."""

    @abstractmethod
    def set(self, namespace: str, key: str, value: Any) -> None:
        """Persist a value under the given namespace and key."""

    @abstractmethod
    def dump_namespace(self, namespace: str) -> Dict[str, Any]:
        """Return all key/value pairs for a namespace."""


__all__ = ["BaseStorage"]
