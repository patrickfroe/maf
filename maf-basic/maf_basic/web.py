"""Simple web chat UI served via the Python standard library."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .app import AgentApp
from .skills import EchoSkill

STATIC_CHAT_FILE = Path(__file__).resolve().parent / "static" / "chat.html"


def _build_agent_app() -> AgentApp:
    app = AgentApp()
    app.register_skill(EchoSkill())
    return app


def _handler_factory(app: AgentApp) -> type[BaseHTTPRequestHandler]:
    class ChatHandler(BaseHTTPRequestHandler):
        def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path != "/":
                self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
                return

            html = STATIC_CHAT_FILE.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/chat":
                self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)

            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON payload."}, status=HTTPStatus.BAD_REQUEST)
                return

            message = str(payload.get("message", "")).strip()
            if not message:
                self._send_json({"error": "Field 'message' must not be empty."}, status=HTTPStatus.BAD_REQUEST)
                return

            answer = app.invoke("EchoSkill", message)
            response = {
                "answer": answer,
                "sources": [
                    {
                        "title": "EchoSkill",
                        "url": "internal://skill/EchoSkill",
                    }
                ],
            }
            self._send_json(response)

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

    return ChatHandler


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    app = _build_agent_app()
    return ThreadingHTTPServer((host, port), _handler_factory(app))


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = create_server(host=host, port=port)
    print(f"Chat UI running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
