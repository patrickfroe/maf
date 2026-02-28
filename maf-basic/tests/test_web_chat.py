"""Tests for the web chat UI HTTP server."""

from __future__ import annotations

import json
import pathlib
import sys
import threading
import urllib.error
import urllib.request

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from maf_basic.web import create_server


def test_get_root_serves_chat_ui() -> None:
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/"
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode("utf-8")

        assert response.status == 200
        assert "id=\"messages\"" in body
        assert "fetch('/chat'" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_post_chat_returns_answer_and_sources() -> None:
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/chat"
        request = urllib.request.Request(
            url,
            data=json.dumps({"message": "Hallo"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert payload["answer"] == "Hallo"
        assert payload["sources"][0]["title"] == "EchoSkill"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_post_chat_requires_message() -> None:
    server = create_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/chat"
        request = urllib.request.Request(
            url,
            data=json.dumps({"message": "   "}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            urllib.request.urlopen(request, timeout=3)
            assert False, "Expected HTTPError for empty message"
        except urllib.error.HTTPError as error:
            payload = json.loads(error.read().decode("utf-8"))
            assert error.code == 400
            assert payload["error"] == "Field 'message' must not be empty."
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
