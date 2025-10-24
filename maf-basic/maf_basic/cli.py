"""Command line interface for the maf-basic demo."""

from __future__ import annotations

from maf_basic.app import AgentApp
from maf_basic.skills.echo import EchoSkill


def main() -> None:
    """Run an interactive session with the echo skill."""
    app = AgentApp()
    skill = EchoSkill()
    app.register_skill(skill)

    print("maf-basic demo – type a message and the agent will echo it back.")
    print("Press Ctrl+C or type 'exit' to quit.\n")

    try:
        while True:
            user_input = input("You: ")
            cleaned = user_input.strip()
            if not cleaned:
                print("(please enter a message)")
                continue
            reply = app.invoke(skill.metadata.name, user_input)
            print(f"Agent: {reply}")
            if cleaned.lower() in {"exit", "quit"}:
                break
    except KeyboardInterrupt:
        print("\nExiting conversation...")

    history = skill.conversation_history(app.storage)
    if history:
        print("\nConversation history saved in storage:")
        for idx, message in enumerate(history, start=1):
            print(f" {idx}. {message}")


if __name__ == "__main__":
    main()
