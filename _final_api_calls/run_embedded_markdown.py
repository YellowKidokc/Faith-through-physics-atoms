#!/usr/bin/env python3
"""Execute a named Python block embedded in a governed Markdown API call."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


BLOCK = re.compile(
    r"```python\s+final_api_python\s*\n(?P<code>.*?)\n```",
    re.DOTALL,
)


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: run_embedded_markdown.py SPEC.md [arguments for embedded call]"
        )
    spec = Path(sys.argv[1]).resolve()
    text = spec.read_text(encoding="utf-8")
    match = BLOCK.search(text)
    if not match:
        raise SystemExit(f"No `python final_api_python` block found in {spec}")

    env = os.environ.copy()
    env["FINAL_API_SPEC_PATH"] = str(spec)
    env["PYTHONUTF8"] = "1"
    with tempfile.TemporaryDirectory(prefix="ftp-final-api-") as temp:
        script = Path(temp) / "embedded_call.py"
        script.write_text(match.group("code") + "\n", encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(script), *sys.argv[2:]],
            cwd=str(spec.parents[1]),
            env=env,
            check=False,
        )
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

