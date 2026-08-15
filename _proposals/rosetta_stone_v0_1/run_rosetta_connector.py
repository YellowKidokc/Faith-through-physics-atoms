#!/usr/bin/env python3
"""Proposal rail: map blind semantic nodes to a declared chain without promotion.

The node extraction run stays blind. This later rail compares each completed node
with a declared schema, retains the raw response, and makes gaps/floating nodes
visible. It never writes to the production ledger, changes a node, or grants a
truth/canon verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import traceback
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
STAGES = ("chain", "proof_stack", "derivative_families")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def api_key() -> str:
    if os.getenv("DEEPSEEK_API_KEY", "").strip():
        return os.environ["DEEPSEEK_API_KEY"].strip()
    env_path = REPO / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("DEEPSEEK_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("DEEPSEEK_API_KEY was not found.")


def call(prompt_text: str, model: str) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return exactly one valid JSON object."},
            {"role": "user", "content": prompt_text},
        ],
        "temperature": 0,
        "max_tokens": 1000,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload, ensure_ascii=True).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            raw = json.loads(response.read().decode("utf-8"))["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"DeepSeek HTTP {exc.code}: {exc.read().decode(errors='replace')}") from exc
    result, end = json.JSONDecoder().raw_decode(raw.lstrip())
    trailing = raw.lstrip()[end:].strip()
    if trailing:
        result["_provider_trailing_text"] = trailing
    return result


def node_payload(node: dict[str, Any], source_receipt: Path) -> dict[str, Any]:
    return {
        "node_id": node["node_id"],
        "coherent_statement": node.get("coherent_statement", ""),
        "plain_statement": node.get("plain_statement", ""),
        "formal_expressions": node.get("formal_expressions", []),
        "scope_text": node.get("scope_text", ""),
        "source_receipt": str(source_receipt),
    }


def prompt_for(stage: str, node: dict[str, Any], schema: dict[str, Any]) -> str:
    subject = node_payload(node, Path("SOURCE_RECEIPT_RECORDED_IN_RECEIPT"))
    if stage == "chain":
        shape = '{"node_id":"...","chain_step":1,"relationship":"supports|contradicts|extends|floating","confidence":0.0,"reason":"one sentence","nearest_step":1}'
        reference = schema["chain"]
        instruction = "Match only against the numbered declared chain steps. Use null for chain_step and nearest_step when no meaningful nearest step exists."
    elif stage == "proof_stack":
        shape = '{"node_id":"...","proof_step_id":"P1|null","role":"direct_support|premise|evidence|counterargument|background|floating","confidence":0.0,"reason":"one sentence"}'
        reference = schema["proof_stack"]
        instruction = "Match only against the declared proof-stack records. A match is a comparison result, not proof of either record."
    else:
        shape = '{"node_id":"...","family_symbol":"G|null","mode":null,"relationship":"supports|extends|contradicts|floating","confidence":0.0,"reason":"one sentence"}'
        reference = schema["derivative_families"]
        instruction = "Match only against declared derivative families. Do not invent a mode or family not present in the reference."
    return f'''You are performing one bounded structural comparison.

{instruction}
Use only the supplied node and reference. Do not use outside knowledge. Do not
assign truth, validity, dependency, admission, canon status, or a final verdict.
If the fit is weak or absent, return floating rather than forcing a match.

Return exactly this JSON shape:
{shape}

DECLARED REFERENCE:
{json.dumps(reference, ensure_ascii=False)}

BLIND SEMANTIC NODE:
{json.dumps(subject, ensure_ascii=False)}
'''


def load_nodes(receipts_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(receipts_dir.glob("*.nodes.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for node in payload.get("result", {}).get("semantic_nodes", []):
            if node.get("node_id"):
                loaded.append((path, node))
    return loaded


def summary(rows: list[dict[str, Any]], schema: dict[str, Any]) -> dict[str, Any]:
    by_stage: dict[str, dict[str, Any]] = {}
    for stage in STAGES:
        results = [row for row in rows if row["stage"] == stage and row["status"] in {"completed", "reused"}]
        values = [row.get("result", {}) for row in results]
        if stage == "chain":
            matched = Counter(str(value.get("chain_step")) for value in values if value.get("chain_step") is not None)
            expected = [str(item["step"]) for item in schema["chain"]]
        elif stage == "proof_stack":
            matched = Counter(str(value.get("proof_step_id")) for value in values if value.get("proof_step_id"))
            expected = [str(item["id"]) for item in schema["proof_stack"]]
        else:
            matched = Counter(str(value.get("family_symbol")) for value in values if value.get("family_symbol"))
            expected = [str(item["symbol"]) for item in schema["derivative_families"]]
        floating = sum(1 for value in values if "floating" in str(value.get("relationship", value.get("role", ""))).lower())
        by_stage[stage] = {
            "completed": len(values),
            "floating": floating,
            "matches": dict(sorted(matched.items())),
            "unmatched_declared_reference": [item for item in expected if item not in matched],
        }
    return {"generated_at": now(), "rows": len(rows), "by_stage": by_stage}


def main() -> None:
    parser = argparse.ArgumentParser(description="Map blind semantic nodes to the declared Rosetta chain.")
    parser.add_argument("semantic_receipts", help="Directory containing AX-*.nodes.json receipt files")
    parser.add_argument("--output-dir", default=str(ROOT / "runs" / "latest"))
    parser.add_argument("--schema", default=str(ROOT / "chain_schema.json"))
    parser.add_argument("--model", default=os.getenv("DEEPSEEK_MODEL") or "deepseek-chat")
    parser.add_argument("--limit", type=int, default=0, help="Limit source nodes; useful for smoke tests.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.25)
    args = parser.parse_args()

    schema_path = Path(args.schema).resolve()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    source_dir = Path(args.semantic_receipts).resolve()
    nodes = load_nodes(source_dir)
    if args.limit:
        nodes = nodes[:args.limit]
    if not nodes:
        raise SystemExit("No completed semantic-node receipts found.")

    output = Path(args.output_dir).resolve()
    prompt_dir, receipt_dir = output / "prompts", output / "receipts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "started_at": now(),
        "source_semantic_receipts": str(source_dir),
        "source_receipt_count": len({str(path) for path, _ in nodes}),
        "node_count": len(nodes),
        "schema": str(schema_path),
        "schema_sha256": sha(schema_path),
        "model": args.model,
        "stages": list(STAGES),
        "boundary": "Proposal comparison only. No source node is changed; no match is proof, admission, canonization, or a truth verdict. This rail does not write to the production SQL ledger.",
    }
    (output / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    rows: list[dict[str, Any]] = []
    total = len(nodes) * len(STAGES)
    position = 0
    for source_receipt, node in nodes:
        for stage in STAGES:
            position += 1
            stem = f"{node['node_id']}.{stage}"
            prompt_path = prompt_dir / f"{stem}.prompt.md"
            receipt_path = receipt_dir / f"{stem}.json"
            prompt_text = prompt_for(stage, node, schema)
            prompt_path.write_text(prompt_text, encoding="utf-8")
            if receipt_path.exists():
                result = json.loads(receipt_path.read_text(encoding="utf-8")).get("result", {})
                status = "reused"
            elif args.dry_run:
                result = {}
                status = "dry_run"
            else:
                try:
                    print(f"[{position}/{total}] {node['node_id']} -> {stage}", flush=True)
                    result = call(prompt_text, args.model)
                    receipt_path.write_text(json.dumps({
                        "run_at": now(), "provider": "deepseek", "model": args.model,
                        "stage": stage, "node_id": node["node_id"],
                        "source_semantic_receipt": str(source_receipt),
                        "source_receipt_sha256": sha(source_receipt),
                        "schema": str(schema_path), "schema_sha256": sha(schema_path),
                        "result": result, "boundary": manifest["boundary"],
                    }, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
                    status = "completed"
                    time.sleep(args.sleep)
                except Exception as exc:
                    (receipt_dir / f"{stem}.error.txt").write_text(str(exc) + "\n" + traceback.format_exc(), encoding="utf-8")
                    result = {}
                    status = "error"
            rows.append({"node_id": node["node_id"], "stage": stage, "status": status, "receipt": str(receipt_path) if receipt_path.exists() else "", "result": result})
    (output / "RUN_INDEX.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    report = summary(rows, schema)
    (output / "CONNECTOR_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "RUN_REPORT.md").write_text(
        "# Rosetta Stone Connector Run\n\n"
        f"- Nodes: `{len(nodes)}`\n- Mapping attempts: `{len(rows)}`\n"
        f"- Statuses: `{dict(Counter(row['status'] for row in rows))}`\n"
        f"- Boundary: {manifest['boundary']}\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "statuses": dict(Counter(row["status"] for row in rows))}, indent=2))


if __name__ == "__main__":
    main()
