"""Small dependency-free GUI/API for reviewing graph edge proposals."""
from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from adversarial_review import PROPOSALS, REVIEWS, load_jsonl, run_reviews
from math_translation import REPO, build_node, find_claim, render_fragment, translate, write_node

UI = Path(__file__).with_name("adversarial_gui.html")


class Handler(BaseHTTPRequestHandler):
    def send_json(self, value: object, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/proposals":
            reviews = {r.get("proposalID"): r for r in load_jsonl(REVIEWS)}
            self.send_json([{**p, "adversarialReview": reviews.get(p.get("proposalID"))} for p in load_jsonl(PROPOSALS)])
        elif path in {"/", "/index.html"}:
            body = UI.read_bytes(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        if route not in {"/api/review", "/api/math/translate"}:
            return self.send_json({"error": "not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            if route == "/api/math/translate":
                source_path, claim = find_claim(str(data.get("claimID", "")))
                provider = data.get("provider", "local")
                result = translate(claim, provider, data.get("endpoint", ""), data.get("model", ""),
                                   os.getenv("MATH_TRANSLATION_API_KEY", ""), data.get("glossary"))
                node = build_node(claim, result, provider, data.get("model", ""))
                response = {"node": node, "html": render_fragment(node)}
                if data.get("write"):
                    output = write_node(source_path, node); output.with_suffix(".html").write_text(response["html"], encoding="utf-8")
                    response["path"] = output.relative_to(REPO).as_posix()
                return self.send_json(response)
            provider = data.get("provider", "local")
            endpoint = data.get("endpoint", "") if provider == "compatible" else ""
            model = data.get("model", "") if provider == "compatible" else ""
            # The browser never sends or stores secrets; configure the key on the server.
            if provider == "compatible" and not (endpoint and model):
                return self.send_json({"error": "endpoint and model are required"}, 400)
            result = run_reviews(provider, data.get("proposalID"), endpoint, model, os.getenv("ADVERSARY_API_KEY", ""))
            self.send_json(result)
        except (ValueError, TypeError) as exc:
            self.send_json({"error": str(exc)}, 400)

    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch adversarial review GUI")
    parser.add_argument("--host", default="127.0.0.1"); parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args(); print(f"Adversarial review GUI: http://{args.host}:{args.port}")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__": main()
