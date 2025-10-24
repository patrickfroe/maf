"""Simple command line interface for interacting with the demo agent."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maf_basic.app import AgentApp  # noqa: E402  (import after sys.path patch)
from maf_basic.skills import (  # noqa: E402
    EchoSkill,
    ManagementSummarySkill,
    WebSearchSkill,
)


def _setup_agent() -> AgentApp:
    """Create and return an ``AgentApp`` with the default skills registered."""

    app = AgentApp()
    app.register_skill(EchoSkill())
    app.register_skill(WebSearchSkill())
    app.register_skill(ManagementSummarySkill())
    return app


def _build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Interact with the demo agent")
    parser.add_argument(
        "--skill",
        default="EchoSkill",
        help="Name of the skill to invoke for each message (default: EchoSkill)",
    )
    parser.add_argument(
        "--exit-commands",
        nargs="*",
        default=("exit", "quit"),
        help="Commands that terminate the session (default: exit quit)",
    )
    return parser


def _normalize_exit_commands(commands: Iterable[str]) -> set[str]:
    return {command.strip().lower() for command in commands if command.strip()}


def run_cli() -> None:
    """Run the interactive CLI loop."""

    parser = _build_parser()
    args = parser.parse_args()

    app = _setup_agent()
    exit_commands = _normalize_exit_commands(args.exit_commands)

    print("Demo Agent CLI. Type your message and press enter. Type 'exit' to quit.")

    while True:
        try:
            user_input = input(">> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nAuf Wiedersehen!")
            break

        if not user_input:
            continue

        if user_input.strip().lower() in exit_commands:
            print("Auf Wiedersehen!")
            break

        try:
            response = app.invoke(args.skill, user_input)
        except KeyError as error:
            print(f"Fehler: {error}")
            continue

        print(response)


if __name__ == "__main__":
    run_cli()
