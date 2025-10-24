"""Entry point for the minimal Microsoft Agent Framework application.

The script loads environment variables, reads configuration values from
``config/settings.yaml`` and instantiates a simple ``AgentApp`` with a single
skill like handler that echoes incoming text back to the caller.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from maf.core import AgentApp  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "settings.yaml"


def load_settings(config_path: Path) -> Dict[str, Any]:
    """Load the YAML configuration file and expand environment variables.

    The helper keeps the structure of the YAML file intact while allowing the
    use of ``${VARNAME}`` placeholders in the configuration values.
    """

    with config_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return _expand_env_values(data)


def _expand_env_values(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _expand_env_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_env_values(item) for item in value]
    if isinstance(value, str):
        return os.path.expandvars(value)
    return value


async def _echo_skill(context: Any, *args: Any, **kwargs: Any) -> str:
    """A tiny asynchronous handler that echoes back textual input.

    The handler is intentionally defensive so it can operate with a wide range
    of context objects that different AgentApp configurations might provide.
    """

    user_text = ""
    if hasattr(context, "input_text"):
        user_text = getattr(context, "input_text") or ""
    elif isinstance(context, dict):
        user_text = str(context.get("text", ""))
    elif args:
        user_text = str(args[0])

    message = f"Echo: {user_text}" if user_text else "Hello from AgentApp!"

    # Some framework contexts expose helper methods to send responses directly.
    if hasattr(context, "send_output") and callable(context.send_output):
        maybe_awaitable = context.send_output(message)
        if asyncio.iscoroutine(maybe_awaitable):
            await maybe_awaitable
        return message

    return message


def _register_echo_skill(app: AgentApp) -> None:
    """Register the echo handler with the instantiated ``AgentApp``.

    The Microsoft Agent Framework offers multiple ways of registering skills
    depending on the chosen abstractions. The helper tries a few of the common
    patterns so the example keeps working across framework versions.
    """

    async def handler(context: Any, *args: Any, **kwargs: Any) -> str:
        return await _echo_skill(context, *args, **kwargs)

    skills = getattr(app, "skills", None)
    if skills is not None:
        if hasattr(skills, "add_function"):
            skills.add_function(
                name="echo",
                description="Echoes back the provided input",
                function=handler,
            )
            return
        if hasattr(skills, "register"):
            try:
                skills.register("echo", handler)
            except TypeError:
                skills.register(name="echo", handler=handler)
            return
        if hasattr(skills, "add"):
            try:
                skills.add("echo", handler)
            except TypeError:
                skills.add(handler)
            return

    if hasattr(app, "register_skill"):
        try:
            app.register_skill("echo", handler)
        except TypeError:
            app.register_skill(name="echo", handler=handler)
        return

    # Fallback: attach the handler as a plain attribute so it can still be used
    # manually in environments where automatic registration is not available.
    setattr(app, "echo", handler)


def create_app() -> AgentApp:
    """Factory that prepares and returns a configured ``AgentApp`` instance."""

    load_dotenv(BASE_DIR / ".env")
    settings = load_settings(CONFIG_FILE)

    app = AgentApp(
        name="minimal-agent",
        description="A minimal AgentApp that echoes user messages.",
    )

    # Store the resolved configuration for later inspection.
    setattr(app, "settings", settings)

    _register_echo_skill(app)

    return app


def main() -> AgentApp:
    """Create the application instance and return it for hosting environments."""

    app = create_app()
    return app


if __name__ == "__main__":
    application = main()
    print("AgentApp initialised:", getattr(application, "name", "minimal-agent"))
