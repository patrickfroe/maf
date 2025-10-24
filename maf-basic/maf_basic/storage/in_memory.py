"""Simple in-memory storage implementation."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BaseStorage


class InMemoryStorage(BaseStorage):
    """Dictionary backed storage that keeps values in memory."""

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, namespace: str, key: str) -> Optional[Any]:
        return self._store.get(namespace, {}).get(key)

    def set(self, namespace: str, key: str, value: Any) -> None:
        namespace_store = self._store.setdefault(namespace, {})
        namespace_store[key] = value

    def dump_namespace(self, namespace: str) -> Dict[str, Any]:
        return dict(self._store.get(namespace, {}))


__all__ = ["InMemoryStorage"]
