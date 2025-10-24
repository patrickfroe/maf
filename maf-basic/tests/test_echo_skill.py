"""Unit tests for the EchoSkill and AgentApp wiring."""

from __future__ import annotations

import pathlib
import sys

import pytest

# Ensure the project root is available on the Python path when the package is not installed.
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maf_basic.app import AgentApp
from maf_basic.skills.echo import EchoSkill
from maf_basic.storage.in_memory import InMemoryStorage


@pytest.fixture()
def app_with_echo() -> AgentApp:
    app = AgentApp(storage=InMemoryStorage())
    echo = EchoSkill()
    app.register_skill(echo)
    return app


def test_echo_skill_returns_same_message(app_with_echo: AgentApp) -> None:
    message = "Hello Agent Framework!"
    response = app_with_echo.invoke("EchoSkill", message)
    assert response == message


def test_echo_skill_stores_history(app_with_echo: AgentApp) -> None:
    app_with_echo.invoke("EchoSkill", "first")
    app_with_echo.invoke("EchoSkill", "second")

    skill = app_with_echo.get_skill("EchoSkill")
    assert isinstance(skill, EchoSkill)

    history = skill.conversation_history(app_with_echo.storage)
    assert history == ["first", "second"]


def test_unknown_skill_raises_error() -> None:
    app = AgentApp(storage=InMemoryStorage())
    with pytest.raises(KeyError):
        app.invoke("unknown", "hi")
