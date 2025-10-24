"""Skill implementations bundled with the demo app."""

from __future__ import annotations

from .echo import EchoSkill
from .management_summary import ManagementSummarySkill
from .web_search import WebSearchSkill

__all__ = ["EchoSkill", "WebSearchSkill", "ManagementSummarySkill"]
