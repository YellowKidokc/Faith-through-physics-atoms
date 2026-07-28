#!/usr/bin/env python3
"""Run the Lane 4 Lean/pill/claim logging pipeline.

This wrapper ties together the existing pieces:

1. Validate Lane 4 atoms.
2. Add the classified Lean corpus pill when its source files are present.
3. Rebuild the Master Equation topbar packet.
4. Add the Lean corpus pill to the final generated packet.
5. Intake the final packet through the live claim runtime.
5. Validate Lane 4 again.
6. Write a durable receipt.

It does not call a claim "Lean proved" by itself. Lean proof status still has to
arrive as an explicit receipt from a compiling Lean run.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "_scripts"
RUNTIME = ROOT / "_runtime"
REPORT_MD = RUNTIME / "LEAN_PILL_CLAIM_PIPELINE_RECEIPT.md"
REPORT_JSON = RUNTIME / "lean_pill_claim_pipeline_receipt.json"
LEAN_CORPUS = Path(r"\\192.168.2.50\h_hp\Desktop 2\LEAN 4\LEAN4_CORPUS_CLASSIFIED.json")
MASTER_PACKET = ROOT / "master-equation" / "11_articles" / "TOPBAR_FILL_PACKET.master-equation.generated.json"


def run_step(name: str, args: list[str], required: bool = True) -> dict:
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return {
        "name": name,
        "required": required,
        "started": started,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "command": args,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def file_state(path: Path) -> dict:
    return {
        "path": str(path),
        "exists": path.exists(),
        "length": path.stat().st_size if path.exists() else 0,
        "lastWriteTime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds") if path.exists() else "",
    }


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    steps: list[dict] = []

    steps.append(run_step("lane4_validate_before", [python, str(SCRIPTS / "lane4_ledger.py"), "validate"]))

    steps.append(run_step("build_topbar_packet", [python, str(SCRIPTS / "build_topbar_packet.py")]))

    if LEAN_CORPUS.exists() and MASTER_PACKET.exists():
        steps.append(run_step("add_lean_corpus_pill", [python, str(SCRIPTS / "add_lean_corpus_pill.py")]))
    else:
        steps.append(
            {
                "name": "add_lean_corpus_pill",
                "required": False,
                "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "returncode": 0,
                "ok": True,
                "command": [python, str(SCRIPTS / "add_lean_corpus_pill.py")],
                "stdout": "Skipped: Lean corpus source or Master Equation packet is not present.",
                "stderr": "",
            }
        )

    if MASTER_PACKET.exists():
        steps.append(run_step("claim_runtime_intake_master_packet", [python, str(SCRIPTS / "claim_runtime.py"), "intake", str(MASTER_PACKET), "--limit", "80"]))
    else:
        steps.append(
            {
                "name": "claim_runtime_intake_master_packet",
                "required": True,
                "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "returncode": 1,
                "ok": False,
                "command": [python, str(SCRIPTS / "claim_runtime.py"), "intake", str(MASTER_PACKET), "--limit", "80"],
                "stdout": "",
                "stderr": "Master Equation topbar packet missing after build.",
            }
        )

    steps.append(run_step("lane4_validate_after", [python, str(SCRIPTS / "lane4_ledger.py"), "validate"]))

    required_failed = [s for s in steps if s["required"] and not s["ok"]]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "passed" if not required_failed else "failed",
        "purpose": "Lean corpus pill, topbar packet rebuild, live claim logging, and Lane 4 validation.",
        "boundary": "This pipeline logs and sorts claims. It does not create Lean proof status unless a Lean proof receipt is explicitly attached.",
        "inputs": {
            "leanCorpus": file_state(LEAN_CORPUS),
            "masterPacket": file_state(MASTER_PACKET),
        },
        "outputs": {
            "liveClaimLedger": file_state(RUNTIME / "live_claim_ledger.jsonl"),
            "frameworkGraphJson": file_state(RUNTIME / "framework_graph.json"),
            "frameworkMindmapHtml": file_state(RUNTIME / "framework_mindmap.html"),
            "receiptMarkdown": str(REPORT_MD),
            "receiptJson": str(REPORT_JSON),
        },
        "steps": steps,
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Lean Pill Claim Pipeline Receipt",
        "",
        f"Generated: {payload['generatedAt']}",
        f"Status: **{payload['status']}**",
        "",
        "## Boundary",
        "",
        payload["boundary"],
        "",
        "## Files",
        "",
        f"- Lean corpus: `{LEAN_CORPUS}` ({'present' if LEAN_CORPUS.exists() else 'missing'})",
        f"- Master packet: `{MASTER_PACKET}` ({'present' if MASTER_PACKET.exists() else 'missing'})",
        f"- Live claim ledger: `{RUNTIME / 'live_claim_ledger.jsonl'}`",
        "",
        "## Steps",
        "",
        "| Step | Required | Result |",
        "|---|---:|---|",
    ]
    for step in steps:
        result = "ok" if step["ok"] else f"failed ({step['returncode']})"
        lines.append(f"| `{step['name']}` | {str(step['required']).lower()} | {result} |")
    lines += [
        "",
        "## Meaning",
        "",
        "```text",
        "Claims can be extracted from the topbar packet and logged automatically.",
        "The Lean corpus pill can be inserted automatically when the classified corpus JSON is available.",
        "Lane 4 validation runs before and after the pipeline.",
        "Lean proof labels still require explicit Lean compile/proof receipts.",
        "```",
    ]
    if required_failed:
        lines += ["", "## Failures", ""]
        for step in required_failed:
            lines += [
                f"### {step['name']}",
                "",
                "```text",
                step["stderr"] or step["stdout"] or "No output.",
                "```",
                "",
            ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT_MD)
    print(f"status={payload['status']}")
    return 0 if not required_failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
